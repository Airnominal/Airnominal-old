/* eslint-disable no-console */

import { getModule, Module, MutationAction, VuexModule } from 'vuex-module-decorators'

import store from '@/store'
import { SettingsModule } from '@/store/modules/settings'
import { displaySnackbar } from '@/utils/snackbar'

// TODO: Add storage

export interface Lesson {
  day: number;
  time: number;
  subject: string;
  class: string;
  teacher: string;
  classroom: string;
}

export interface Substitution extends Lesson {
  date: string;
  'original-teacher': string;
  'original-classroom': string;
}

export interface DisplayedLesson {
  day: number;
  time: number;
  subjects: string[];
  classes: string[];
  teachers: string[];
  classrooms: string[];
  substitution: boolean;
}

export interface LunchSchedule {
  class: string;
  date: string;
  time: string;
  location: string;
  notes: string | null;
}

export interface Menu {
  date: string;
  snack: {
    normal: string,
    vegetarian: string,
    poultry: string,
    fruitvegetable: string
  };
  lunch: {
    normal: string,
    vegetarian: string
  }
}

export interface Document {
  data: string;
  type: string;
  url: string;
  description: string;
}

export function getLessonId (substitution: Lesson): string {
  return `${substitution.day}-${substitution.time}-${substitution.class}-${substitution.teacher}`
}

export function getSubstitutionId (substitution: Substitution): string {
  return `${substitution.day}-${substitution.time}-${substitution.class}-${substitution['original-teacher']}`
}

export async function updateAllData (): Promise<void> {
  await Promise.all([
    StorageModule.updateLists(true),
    StorageModule.updateTimetable(true),
    StorageModule.updateEmptyClassrooms(true),
    // StorageModule.updateSubstitutions(true),
    // StorageModule.updateLunchSchedule(true),
    // StorageModule.updateMenus(true),
    StorageModule.updateDocuments(true)
  ])

  displaySnackbar('Podatki posodobljeni')
}

class HTTPError extends Error {
  status: number

  constructor (message: string, status: number) {
    super(message)

    this.name = 'HTTPError'
    this.status = status
  }
}

async function fetchHandle (input: RequestInfo, init?: RequestInit): Promise<Response> {
  const response = await fetch(input, init)

  if (!response.ok) {
    throw new HTTPError(`Invalid response status from the API: ${response.status}`, response.status)
  }

  return response
}

@Module({ name: 'storage', dynamic: true, preserveState: true, preserveStateType: 'mergeReplaceArrays', store })
class Storage extends VuexModule {
  lastUpdated: Date | null = null

  classList: string[] | null = null
  teacherList: string[] | null = null
  classroomList: string[] | null = null

  timetable: Lesson[] | null = null
  _substitutions: Substitution[][] | null = null
  emptyClassrooms: Lesson[] | null = null

  lunchSchedule: [string, LunchSchedule[]][] | null = null
  menus: [string, Menu][] | null = null

  documents: Document[] | null = null

  get substitutions (): Map<string, Substitution[]> {
    const substitutionMap = new Map()

    // Add keys to substitutions so they can be found more quickly
    for (const substitution of (this._substitutions?.flat() || [])) {
      if (!substitution) continue

      const substitutionId = getSubstitutionId(substitution)
      substitutionMap.set(substitutionId, (substitutionMap.get(substitutionId) || []).concat(substitution))
    }

    return substitutionMap
  }

  @MutationAction
  async updateLists (forceUpdate = false) {
    const isStoredLocally = 'storage' in localStorage && this.classList
    const shouldUpdateStorage = !isStoredLocally || !('settings' in localStorage) || SettingsModule.enableUpdateOnLoad

    if (!navigator.onLine) {
      displaySnackbar('Internetna povezava ni na voljo')
      return
    }
    if (!forceUpdate && !shouldUpdateStorage) {
      return
    }

    try {
      const responses = await Promise.all([
        fetchHandle(process.env.VUE_APP_BACKEND + '/list/classes'),
        fetchHandle(process.env.VUE_APP_BACKEND + '/list/teachers'),
        fetchHandle(process.env.VUE_APP_BACKEND + '/list/classrooms')
      ])

      const [classList, teacherList, classroomList] = await Promise.all(responses.map(response => response.json()))
      const lastUpdated = new Date()

      return { classList, teacherList, classroomList, lastUpdated }
    } catch (error) {
      displaySnackbar('Napaka pri pridobivanju podatkov')
      console.error(error)
    }
  }

  @MutationAction
  async updateTimetable (forceUpdate = false) {
    const isStoredLocally = 'storage' in localStorage && this.timetable
    const shouldUpdateStorage = !isStoredLocally || !('settings' in localStorage) || SettingsModule.enableUpdateOnLoad

    if (!navigator.onLine) {
      displaySnackbar('Internetna povezava ni na voljo')
      return
    }

    if (!forceUpdate && !shouldUpdateStorage) {
      return
    }

    try {
      const response = await fetchHandle(process.env.VUE_APP_BACKEND + '/timetable')
      return { timetable: await response.json(), lastUpdated: new Date() }
    } catch (error) {
      displaySnackbar('Napaka pri pridobivanju podatkov')
      console.error(error)
    }
  }

  @MutationAction
  async updateEmptyClassrooms (forceUpdate = false) {
    const isStoredLocally = 'storage' in localStorage && this.emptyClassrooms
    const shouldUpdateStorage = !isStoredLocally || !('settings' in localStorage) || SettingsModule.enableUpdateOnLoad

    if (!navigator.onLine) {
      displaySnackbar('Internetna povezava ni na voljo')
      return
    }

    if (!forceUpdate && !shouldUpdateStorage) {
      return
    }

    try {
      const response = await fetchHandle(process.env.VUE_APP_BACKEND + '/timetable/classrooms/empty')
      return { emptyClassrooms: await response.json(), lastUpdated: new Date() }
    } catch (error) {
      displaySnackbar('Napaka pri pridobivanju podatkov')
      console.error(error)
    }
  }

  @MutationAction
  async updateDocuments (forceUpdate = false) {
    const isStoredLocally = 'storage' in localStorage && this.documents
    const shouldUpdateStorage = !isStoredLocally || !('settings' in localStorage) || SettingsModule.enableUpdateOnLoad

    if (!navigator.onLine) {
      displaySnackbar('Internetna povezava ni na voljo')
      return
    }

    if (!forceUpdate && !shouldUpdateStorage) {
      return
    }

    try {
      const response = await fetchHandle(process.env.VUE_APP_BACKEND + '/documents')
      return { documents: await response.json(), lastUpdated: new Date() }
    } catch (error) {
      displaySnackbar('Napaka pri pridobivanju podatkov')
      console.error(error)
    }
  }
}

export const StorageModule = getModule(Storage)
