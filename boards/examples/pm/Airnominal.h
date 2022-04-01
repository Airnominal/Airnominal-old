#include <MsgPack.h>
#include "Config.h"

namespace AirNom
{
  MsgPack::str_t key = STATION_KEY;
  MsgPack::str_t iST = STATION_ID;

  struct Measurement{
    MsgPack::str_t key_k {"k"}; MsgPack::str_t k;
    MsgPack::str_t key_iST {"iST"}; MsgPack::str_t iST;
    MsgPack::str_t key_iSE {"iSE"}; MsgPack::str_t iSE;
    MsgPack::str_t key_v {"v"}; float v;
    MsgPack::str_t key_lat {"lat"}; float lat;
    MsgPack::str_t key_lon {"lon"}; float lon;
    MSGPACK_DEFINE_MAP(key_k, k, key_iST, iST, key_iSE, iSE, key_v, v, key_lat, lat, key_lon, lon);
  };
  Measurement measurements[MAXmesSize];
  int curr = 0;
  void createMeasurement(MsgPack::str_t iSE, float v, float lat, float lon){
    if(curr == MAXmesSize){
      return;
      };
    Measurement mes;
    mes.k = key;
    mes.iST = iST;
    mes.iSE = iSE;
    mes.v = v;
    mes.lat = lat;
    mes.lon = lon;
    measurements[curr] = mes;
    curr++;
    };
  
  MsgPack::Packer send(){
    MsgPack::Packer packer;
    packer.pack(measurements, (size_t)(curr));
    curr = 0;
    return packer;
  };
}
using namespace AirNom;
