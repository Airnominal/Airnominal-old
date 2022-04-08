<template>
  <div class="registration px-4 pt-4">
    <h2 class="pb-2">Register Station</h2>

    <div v-if="!this.stationRegistered">
      <v-form
        ref="form"
        v-model="formValid"
        lazy-validation>
        <v-text-field
          :rules="[v => !!v || 'Name is required!']"
          v-model="stationName"
          label="Name"
          maxlength="200"
          required></v-text-field>

        <v-text-field
          v-model="stationDescription"
          label="Description"
          maxlength="200"
          required></v-text-field>

        <v-select
          v-model="stationMeasurementTypes"
          :items="availableMeasurementTypes"
          hint="Select all sensors the station provides"
          label="Sensors"
          persistent-hint
          multiple></v-select>

        <div class="pt-6 text-justify">
          <strong>Important: </strong>
          Once you create a station, you cannot modify or remove it. This includes not being able to
          rename the station or add new sensors. Please be sure the provided information is correct
          before submitting a form.
        </div>

        <div class="py-2 text-justify">
          As the platform is currently in the early stages of development, we cannot guarantee 100%
          availability and reliability of the service. As such, your registered stations and measurements
          may not be stored permanently. We are working hard to improve the stability of the service
          and implement missing station management features.
        </div>

        <v-checkbox
          :rules="[v => !!v || 'You must agree to continue!']"
          label="Do you agree?"
          required></v-checkbox>

        <v-btn
          :disabled="!formValid"
          color="primary"
          class="mt-3"
          @click="submitForm">
          Submit
        </v-btn>
      </v-form>
    </div>

    <div v-else>
      <div class="text-justify pb-3">
        Your station has been successfully registered to the server. Please use the following
        config to set up it up. Make sure you save the config as you will not be able to view
        it again after closing this page.
      </div>

      <div class="text-justify pb-3">
        Please check the <a href="https://github.com/ChristofferNorgaard/Airnominal/tree/main/boards#readme"
        target="_blank">documentation</a> for more details about setting up the station.
      </div>

      <kbd>{{ JSON.stringify(this.stationConfig) }}</kbd>
    </div>
  </div>
</template>

<style lang="scss">
// Add back top padding that is removed by a dialog
.v-dialog > .v-card > .v-card__text {
  padding: 16px 24px 20px !important;
}

// Center registration page
.registration {
  margin: 0 auto;
  max-width: 40rem;
}
</style>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator'

import { displaySnackbar } from '@/utils/snackbar'
import { fetchHandle } from '@/utils/fetch'

/**
 * Defines type of "measurement type" object.
 *
 * At least one of `id`/`name` properties is guaranteed to exist.
 * Property `unit` is not necessarily provided.
 */
type TypeType = {
  id?: string,
  name?: string,
  unit?: string,
}

@Component
export default class RegisterStation extends Vue {
  formValid = true
  stationRegistered = false
  stationConfig: Object = []

  stationName: string | null = null
  stationDescription: string | null = null
  stationMeasurementTypes: string[] = []

  availableMeasurementTypes: { text: string, value: string }[] = []

  /**
   * Fetch available measurement types from the API.
   */
  async getAvailableMeasurementTypes (): Promise<{ text: string, value: string }[]> {
    if (!navigator.onLine) {
      displaySnackbar('No internet connection')
      return []
    }

    let types: TypeType[]

    try {
      const response = await fetchHandle(process.env.VUE_APP_BACKEND + '/platforms/measurement/type')
      types = await response.json()
    } catch (error) {
      displaySnackbar('Error while accessing available measurement types')
      console.error(error)
      return []
    }

    const result: { text: string; value: string }[] | PromiseLike<{ text: string; value: string }[]> = []

    for (const type of types) {
      const typeId = type.id ?? type.name
      const typeName = type.name ?? type.id
      const typeUnit = type.unit

      result.push({
        text: typeUnit ? `${typeName} (${typeUnit})` : typeName!,
        value: typeId!,
      })
    }

    return result
  }

  async created (): Promise<void> {
    // Set page title
    document.title = process.env.VUE_APP_TITLE + ' – Register Station'
    this.$emit('setPageTitle', 'Register Station')
    this.$emit('setPullToRefreshAllowed', false)

    // Get measurement types from the API
    this.availableMeasurementTypes = await this.getAvailableMeasurementTypes()
  }

  async submitForm (): Promise<void> {
    // @ts-ignore
    if (!this.$refs.form.validate()) return

    let status: { success: boolean, config: string, error: string }
    try {
      const response = await fetchHandle(process.env.VUE_APP_BACKEND + '/platforms/new', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: this.stationName,
          description: this.stationDescription,
          sensors: this.stationMeasurementTypes.map(type => ({
            name: type,
            mes_type: type,
          }))
        })
      })
      status = await response.json()
    } catch (error) {
      displaySnackbar('Error while registering the station')
      console.error(error)
      return
    }

    if (!status.success) {
      displaySnackbar(status.error)
      return
    }

    this.stationConfig = JSON.parse(status.config)
    this.stationRegistered = true
  }
}
</script>
