#!/usr/bin/env python3
"""
Free Fire Wardrobe & Loadout Manager - FIXED GRID
- Fixed 3 columns on phone
- Fixed CSS issues
- 3 domains for all endpoints
"""

import io
import gzip
import json
import base64
import binascii
import traceback
from collections import defaultdict
from flask import Flask, render_template_string, request, session, jsonify
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'

# ==================== PROTOBUF DEFINITIONS ====================
_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13MajorLoginReq.proto\"\xfa\n\n\nMajorLogin\x12\x12\n\nevent_time\x18\x03 \x01(\t\x12\x11\n\tgame_name\x18\x04 \x01(\t\x12\x13\n\x0bplatform_id\x18\x05 \x01(\x05\x12\x16\n\x0e\x63lient_version\x18\x07 \x01(\t\x12\x17\n\x0fsystem_software\x18\x08 \x01(\t\x12\x17\n\x0fsystem_hardware\x18\t \x01(\t\x12\x18\n\x10telecom_operator\x18\n \x01(\t\x12\x14\n\x0cnetwork_type\x18\x0b \x01(\t\x12\x14\n\x0cscreen_width\x18\x0c \x01(\r\x12\x15\n\rscreen_height\x18\r \x01(\r\x12\x12\n\nscreen_dpi\x18\x0e \x01(\t\x12\x19\n\x11processor_details\x18\x0f \x01(\t\x12\x0e\n\x06memory\x18\x10 \x01(\r\x12\x14\n\x0cgpu_renderer\x18\x11 \x01(\t\x12\x13\n\x0bgpu_version\x18\x12 \x01(\t\x12\x18\n\x10unique_device_id\x18\x13 \x01(\t\x12\x11\n\tclient_ip\x18\x14 \x01(\t\x12\x10\n\x08language\x18\x15 \x01(\t\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x14\n\x0copen_id_type\x18\x17 \x01(\t\x12\x13\n\x0b\x64\x65vice_type\x18\x18 \x01(\t\x12\'\n\x10memory_available\x18\x19 \x01(\x0b\x32\r.GameSecurity\x12\x14\n\x0c\x61\x63\x63\x65ss_token\x18\x1d \x01(\t\x12\x17\n\x0fplatform_sdk_id\x18\x1e \x01(\x05\x12\x1a\n\x12network_operator_a\x18) \x01(\t\x12\x16\n\x0enetwork_type_a\x18* \x01(\t\x12\x1c\n\x14\x63lient_using_version\x18\x39 \x01(\t\x12\x1e\n\x16\x65xternal_storage_total\x18< \x01(\x05\x12\"\n\x1a\x65xternal_storage_available\x18= \x01(\x05\x12\x1e\n\x16internal_storage_total\x18> \x01(\x05\x12\"\n\x1ainternal_storage_available\x18? \x01(\x05\x12#\n\x1bgame_disk_storage_available\x18@ \x01(\x05\x12\x1f\n\x17game_disk_storage_total\x18\x41 \x01(\x05\x12%\n\x1d\x65xternal_sdcard_avail_storage\x18\x42 \x01(\x05\x12%\n\x1d\x65xternal_sdcard_total_storage\x18\x43 \x01(\x05\x12\x10\n\x08login_by\x18I \x01(\x05\x12\x14\n\x0clibrary_path\x18J \x01(\t\x12\x12\n\nreg_avatar\x18L \x01(\x05\x12\x15\n\rlibrary_token\x18M \x01(\t\x12\x14\n\x0c\x63hannel_type\x18N \x01(\x05\x12\x10\n\x08\x63pu_type\x18O \x01(\x05\x12\x18\n\x10\x63pu_architecture\x18Q \x01(\t\x12\x1b\n\x13\x63lient_version_code\x18S \x01(\t\x12\x14\n\x0cgraphics_api\x18V \x01(\t\x12\x1d\n\x15supported_astc_bitset\x18W \x01(\r\x12\x1a\n\x12login_open_id_type\x18X \x01(\x05\x12\x18\n\x10\x61nalytics_detail\x18Y \x01(\x0c\x12\x14\n\x0cloading_time\x18\\ \x01(\r\x12\x17\n\x0frelease_channel\x18] \x01(\t\x12\x12\n\nextra_info\x18^ \x01(\t\x12 \n\x18\x61ndroid_engine_init_flag\x18_ \x01(\r\x12\x0f\n\x07if_push\x18\x61 \x01(\x05\x12\x0e\n\x06is_vpn\x18\x62 \x01(\x05\x12\x1c\n\x14origin_platform_type\x18\x63 \x01(\t\x12\x1d\n\x15primary_platform_type\x18\x64 \x01(\t\"5\n\x0cGameSecurity\x12\x0f\n\x07version\x18\x06 \x01(\x05\x12\x14\n\x0chidden_value\x18\x08 \x01(\x04\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'MajorLoginReq_pb2', _globals)
MajorLogin = _globals['MajorLogin']
GameSecurity = _globals['GameSecurity']

DESCRIPTOR2 = _descriptor_pool.Default().AddSerializedFile(b'\n\x13MajorLoginRes.proto\"|\n\rMajorLoginRes\x12\x13\n\x0b\x61\x63\x63ount_uid\x18\x01 \x01(\x04\x12\x0e\n\x06region\x18\x02 \x01(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\x0b\n\x03url\x18\n \x01(\t\x12\x11\n\ttimestamp\x18\x15 \x01(\x03\x12\x0b\n\x03key\x18\x16 \x01(\x0c\x12\n\n\x02iv\x18\x17 \x01(\x0c\x62\x06proto3')
_globals2 = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR2, _globals2)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR2, 'MajorLoginRes_pb2', _globals2)
MajorLoginRes = _globals2['MajorLoginRes']

# ==================== API ENDPOINTS (3 DOMAINS EACH) ====================
DOMAINS = [
    "client.ind.freefiremobile.com",
    "client.us.freefiremobile.com", 
    "clientbp.ggpolarbear.com"
]

GET_BACKPACK_URLS = [f"https://{domain}/GetBackpack" for domain in DOMAINS]
GET_PERSONAL_SHOW_URLS = [f"https://{domain}/GetPlayerPersonalShow" for domain in DOMAINS]
CHANGE_CLOTHES_URLS = [f"https://{domain}/ChangeClothes" for domain in DOMAINS]
SELECT_LOADOUT_URLS = [f"https://{domain}/SelectPresetLoadout" for domain in DOMAINS]

# ==================== ENCRYPTION KEYS ====================
AES_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
AES_IV = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

# ==================== BASE LOADOUT PAYLOAD ====================
BASE_ENC_HEX = "DBDB005FDC6C0AAC203E92ED23D6D05489F20CBE81D070DEA311216E9D09C5D79E61345A767FDCB1DBD1A46A103661F58C9CBC6B1C53FE01F6D29FD981CE86A2AD80683FA57BA9277EFE55DA5EC92E0BA774EAF3C5CCB6FAB94869A28A988CB5819F8F7064538331D8E31FE5DC9217D6"
BASE_ENC = binascii.unhexlify(BASE_ENC_HEX)
OLD_CHAR_ID = 102000015

def encode_varint(value: int) -> bytes:
    result = []
    while True:
        byte = value & 0x7F
        value >>= 7
        if value == 0:
            result.append(byte)
            break
        result.append(byte | 0x80)
    return bytes(result)

OLD_VARINT = encode_varint(OLD_CHAR_ID)

def encrypt_aes(data: bytes) -> bytes:
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    return cipher.encrypt(pad(data, AES.block_size))

def decrypt_aes_cbc(data: bytes) -> bytes:
    try:
        cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
        return unpad(cipher.decrypt(data), AES.block_size)
    except Exception:
        return None

def encrypt_aes_cbc(data: bytes) -> bytes:
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    padded = pad(data, AES.block_size)
    return cipher.encrypt(padded)

# ==================== TYPE MAPPING ====================
TYPE_TO_SLOT = {
    'Head': 'Head', 'Hair': 'Head', 'Top': 'Top', 'Bottom': 'Bottom',
    'Shoe': 'Shoes', 'Shoes': 'Shoes', 'Mask': 'Mask', 'Face': 'Mask',
}

SLOT_ORDER = ['Mask', 'Top', 'Bottom', 'Shoes', 'Head']
SLOT_ICONS = {'Mask': '😷', 'Top': '👕', 'Bottom': '👖', 'Shoes': '👟', 'Head': '🎭'}

# ==================== MAJOR LOGIN ====================
def build_major_login(open_id: str, access_token: str, platform_type: int) -> bytes:
    major = MajorLogin()
    major.event_time = "2025-03-23 12:00:00"
    major.game_name = "free fire"
    major.platform_id = 1
    major.client_version = "1.126.3"
    major.system_software = "Android OS 9 / API-28"
    major.system_hardware = "Handheld"
    major.telecom_operator = "Verizon"
    major.network_type = "WIFI"
    major.screen_width = 1920
    major.screen_height = 1080
    major.screen_dpi = "280"
    major.processor_details = "ARM64 FP ASIMD AES VMH"
    major.memory = 3003
    major.gpu_renderer = "Adreno (TM) 640"
    major.gpu_version = "OpenGL ES 3.1"
    major.unique_device_id = "Google|34a7dcdf-a7d5-4cb6-8d7e-3b0e448a0c57"
    major.client_ip = "223.191.51.89"
    major.language = "en"
    major.open_id = open_id
    major.open_id_type = "4"
    major.device_type = "Handheld"
    major.memory_available.version = 55
    major.memory_available.hidden_value = 81
    major.access_token = access_token
    major.platform_sdk_id = 1
    major.network_operator_a = "Verizon"
    major.network_type_a = "WIFI"
    major.client_using_version = "7428b253defc164018c604a1ebbfebdf"
    major.external_storage_total = 36235
    major.external_storage_available = 31335
    major.internal_storage_total = 2519
    major.internal_storage_available = 703
    major.game_disk_storage_available = 25010
    major.game_disk_storage_total = 26628
    major.external_sdcard_avail_storage = 32992
    major.external_sdcard_total_storage = 36235
    major.login_by = 3
    major.library_path = "/data/app/com.dts.freefireth/base.apk"
    major.reg_avatar = 1
    major.library_token = "5b892aaabd688e571f688053118a162b|base.apk"
    major.channel_type = 3
    major.cpu_type = 2
    major.cpu_architecture = "64"
    major.client_version_code = "2019118695"
    major.graphics_api = "OpenGLES2"
    major.supported_astc_bitset = 16383
    major.login_open_id_type = 4
    major.analytics_detail = b"FwQVTgUPX1UaUllDDwcWCRBpWA0FUgsvA1snWlBaO1kFYg=="
    major.loading_time = 13564
    major.release_channel = "android"
    major.extra_info = "KqsHTymw5/5GB23YGniUYN2/q47GATrq7eFeRatf0NkwLKEMQ0PK5BKEk72dPflAxUlEBir6Vtey83XqF593qsl8hwY="
    major.android_engine_init_flag = 110009
    major.if_push = 1
    major.is_vpn = 1
    major.origin_platform_type = str(platform_type)
    major.primary_platform_type = str(platform_type)
    return major.SerializeToString()

def get_jwt_from_access_token(access_token: str):
    inspect_url = f"https://100067.connect.garena.com/oauth/token/inspect?token={access_token}"
    try:
        insp_resp = requests.get(inspect_url, timeout=10)
        if insp_resp.status_code != 200:
            return None, f"Failed to inspect token: HTTP {insp_resp.status_code}"
        insp_data = insp_resp.json()
        open_id = insp_data.get('open_id')
        if not open_id:
            return None, "open_id not found"
    except Exception as e:
        return None, f"Inspect failed: {str(e)}"

    platform_types = [2, 3, 4, 6, 8]
    for pt in platform_types:
        try:
            payload = build_major_login(open_id, access_token, pt)
            encrypted_payload = encrypt_aes(payload)
            url = "https://loginbp.ggblueshark.com/MajorLogin"
            headers = {
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 11)",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "Content-Type": "application/x-www-form-urlencoded",
                "X-Unity-Version": "2018.4.11f1",
                "X-GA": "v1 1",
                "ReleaseVersion": "OB54"
            }
            resp = requests.post(url, data=encrypted_payload, headers=headers, timeout=10)
            if resp.status_code == 200:
                major_res = MajorLoginRes()
                major_res.ParseFromString(resp.content)
                if major_res.token:
                    return major_res.token, None
        except Exception as e:
            continue
    return None, "MajorLogin failed"

# ==================== PROTOBUF PARSING ====================
def decode_varint_proto(data, offset):
    value = 0
    shift = 0
    while True:
        if offset >= len(data):
            raise ValueError("Truncated")
        b = data[offset]
        value |= (b & 0x7F) << shift
        offset += 1
        if not (b & 0x80):
            break
        shift += 7
    return value, offset

def parse_one_message(data, start):
    fields = []
    idx = start
    while idx < len(data):
        try:
            key, idx = decode_varint_proto(data, idx)
        except ValueError:
            break
        field_num = key >> 3
        wire_type = key & 0x07

        if wire_type == 0:
            value, idx = decode_varint_proto(data, idx)
            fields.append({'num': field_num, 'type': 0, 'value': value, 'nested': None})
        elif wire_type == 1:
            if idx + 8 > len(data):
                raise ValueError("Truncated")
            value = int.from_bytes(data[idx:idx+8], 'little')
            idx += 8
            fields.append({'num': field_num, 'type': 1, 'value': value, 'nested': None})
        elif wire_type == 2:
            length, idx = decode_varint_proto(data, idx)
            if idx + length > len(data):
                return fields, idx
            raw = data[idx:idx+length]
            idx += length
            nested = None
            try:
                nested, _ = parse_one_message(raw, 0)
            except Exception:
                pass
            fields.append({'num': field_num, 'type': 2, 'value': raw, 'nested': nested})
        elif wire_type == 5:
            if idx + 4 > len(data):
                raise ValueError("Truncated")
            value = int.from_bytes(data[idx:idx+4], 'little')
            idx += 4
            fields.append({'num': field_num, 'type': 5, 'value': value, 'nested': None})
        else:
            raise ValueError(f"Unsupported wire type {wire_type}")
    return fields, idx

def collect_item_ids(fields):
    ids = []
    for f in fields:
        if f['num'] == 3 and f['type'] == 2 and f['nested'] is not None:
            for sub in f['nested']:
                if sub['num'] == 1 and sub['type'] == 0:
                    ids.append(sub['value'])
        if f['nested'] is not None:
            ids.extend(collect_item_ids(f['nested']))
    return ids

def parse_character_and_equipped(data):
    character_id = None
    equipped = {}
    pet_id = None
    loadout = {}
    
    try:
        fields, _ = parse_one_message(data, 0)
        for f in fields:
            if f['num'] == 2 and f['type'] == 2 and f['nested'] is not None:
                for sub in f['nested']:
                    if sub['num'] == 1:
                        character_id = sub['value']
                    if sub['num'] == 5 and sub['type'] == 2 and sub['nested'] is not None:
                        slot_index = None
                        item_id = None
                        for item_field in sub['nested']:
                            if item_field['num'] == 1:
                                slot_index = item_field['value']
                            if item_field['num'] == 2:
                                item_id = item_field['value']
                        if slot_index is not None and item_id is not None:
                            equipped[slot_index] = item_id
            
            if f['num'] == 6 and f['type'] == 2 and f['nested'] is not None:
                for sub in f['nested']:
                    if sub['num'] == 1:
                        loadout['preset_id'] = sub['value']
                    if sub['num'] == 2:
                        loadout['character_id'] = sub['value']
                    if sub['num'] == 4:
                        pet_id = sub['value']
        
        slot_map = {1: 'Mask', 2: 'Top', 3: 'Bottom', 4: 'Shoes', 5: 'Head'}
        equipped_items = {}
        for idx, iid in equipped.items():
            if idx in slot_map:
                equipped_items[slot_map[idx]] = iid
        
        return character_id, equipped_items, pet_id, loadout
    except Exception as e:
        return None, {}, None, {}

def load_item_database():
    try:
        with open("data.json", "r", encoding="utf-8") as f:
            items = json.load(f)
        item_map = {}
        for item in items:
            iid = item.get('itemID')
            if iid is not None:
                item_map[iid] = item
        return item_map
    except Exception as e:
        return {}

# ==================== API CALLS ====================
def fetch_character_and_equipped(token, uid):
    def enc_uid(uid):
        e = []
        uid = int(uid)
        while uid:
            e.append((uid & 0x7F) | (0x80 if uid > 0x7F else 0))
            uid >>= 7
        return bytes(e).hex()

    edata = enc_uid(uid)
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    payload_hex = cipher.encrypt(pad(bytes.fromhex(f"08{edata}1007"), AES.block_size)).hex()
    payload = bytes.fromhex(payload_hex)

    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; Android 9)",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Unity-Version": "2018.4.11f1",
        "X-GA": "v1 1",
        "ReleaseVersion": "OB54"
    }

    for url in GET_PERSONAL_SHOW_URLS:
        try:
            resp = requests.post(url, headers=headers, data=payload, timeout=15)
            if resp.status_code == 200:
                raw = resp.content
                plain = decrypt_aes_cbc(raw)
                data = plain if plain is not None else raw
                char_id, equipped, pet_id, loadout = parse_character_and_equipped(data)
                if char_id is not None:
                    return char_id, equipped, pet_id, loadout, None
        except Exception:
            continue
    return None, None, None, None, "All endpoints failed"

def fetch_vault(token):
    BODY_BYTES = bytes.fromhex("1a725b2c56ec52ba7d09623454c0a003")
    all_ids = set()

    for url in GET_BACKPACK_URLS:
        headers = {
            "Host": url.split('/')[2],
            "User-Agent": "UnityPlayer/2022.3.47f1",
            "Accept": "*/*",
            "Accept-Encoding": "deflate, gzip",
            "Authorization": f"Bearer {token}",
            "X-GA": "v1 1",
            "ReleaseVersion": "OB54",
            "Content-Type": "application/x-www-form-urlencoded",
            "X-Unity-Version": "2022.3.47f1"
        }
        try:
            response = requests.post(url, headers=headers, data=BODY_BYTES, timeout=15)
            if response.status_code == 200:
                raw = response.content
                plain = decrypt_aes_cbc(raw)
                data = plain if plain is not None else raw
                fields, _ = parse_one_message(data, 0)
                ids = collect_item_ids(fields)
                all_ids.update(ids)
        except Exception:
            continue
    
    return list(all_ids), None if all_ids else "No items found"

def apply_change_clothes(token, avatar_id, skill_ids):
    dec = [format(0x80 + i, '02x') for i in range(128)]
    x_list = ['1'] + [format(i, '02x') for i in range(1, 128)]
    
    def encrypt_id(num):
        if num == 0:
            return "0000000000"
        x = float(num)
        x = x / 128
        if x > 128:
            x = x / 128
            if x > 128:
                x = x / 128
                if x > 128:
                    x = x / 128
                    strx = int(x)
                    y = (x - strx) * 128
                    stry = int(y)
                    z = (y - stry) * 128
                    strz = int(z)
                    n = (z - strz) * 128
                    strn = int(n)
                    m = (n - strn) * 128
                    return dec[int(m)] + dec[int(n)] + dec[int(z)] + dec[int(stry)] + x_list[int(strx)]
                else:
                    strx = int(x)
                    y = (x - strx) * 128
                    stry = int(y)
                    z = (y - stry) * 128
                    strz = int(z)
                    n = (z - strz) * 128
                    strn = int(n)
                    return dec[int(n)] + dec[int(z)] + dec[int(stry)] + x_list[int(strx)]
        return "0000000000"

    encrypted_skills_hex = ''.join(encrypt_id(sid) for sid in skill_ids)
    field2_bytes = bytes.fromhex(encrypted_skills_hex)
    field1 = bytes([0x08]) + encode_varint(avatar_id)
    field2 = bytes([0x12, len(field2_bytes)]) + field2_bytes
    field3 = bytes([0x18]) + encode_varint(50)
    protobuf = field1 + field2 + field3
    encrypted_payload = encrypt_aes_cbc(protobuf)

    headers = {
        "Accept-Encoding": "gzip",
        "Authorization": f"Bearer {token}",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "ReleaseVersion": "OB54",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9)",
        "X-GA": "v1 1",
        "X-Unity-Version": "2018.4.11f1",
    }

    for url in CHANGE_CLOTHES_URLS:
        try:
            response = requests.post(url, data=encrypted_payload, headers=headers, timeout=30)
            if response.status_code == 200:
                return True, None
        except Exception:
            continue
    return False, "All ChangeClothes endpoints failed"

def apply_select_loadout(token, new_character_id):
    plain = decrypt_aes_cbc(BASE_ENC)
    if plain is None:
        return False, "Failed to decrypt"
    
    new_varint = encode_varint(new_character_id)
    modified_plain = plain.replace(OLD_VARINT, new_varint)
    encrypted = encrypt_aes_cbc(modified_plain)
    
    headers = {
        "User-Agent": "UnityPlayer/2022.3.47f1",
        "Accept": "*/*",
        "Accept-Encoding": "deflate, gzip",
        "Authorization": f"Bearer {token}",
        "X-GA": "v1 1",
        "ReleaseVersion": "OB54",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Unity-Version": "2022.3.47f1",
    }
    
    for url in SELECT_LOADOUT_URLS:
        try:
            response = requests.post(url, data=encrypted, headers=headers, timeout=30)
            if response.status_code == 200:
                return True, None
        except Exception:
            continue
    return False, "All SelectPresetLoadout endpoints failed"

# ==================== HTML TEMPLATE (FIXED GRID) ====================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes, viewport-fit=cover">
    <title>FF Wardrobe Manager</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
            background: #0a192f; 
            color: #e6f1ff; 
            padding-bottom: 80px; 
        }
        .header { 
            background: linear-gradient(135deg, #0a192f, #112240); 
            padding: 16px 20px; 
            position: sticky; 
            top: 0; 
            z-index: 100; 
            border-bottom: 2px solid #64ffda; 
        }
        .header h1 { font-size: 1.5rem; color: #64ffda; display: flex; align-items: center; gap: 8px; }
        .token-section { background: #112240; margin: 16px; padding: 16px; border-radius: 16px; border: 1px solid #64ffda; }
        .token-input { width: 100%; padding: 14px; background: #1e3a5f; border: 1px solid #64ffda; border-radius: 12px; color: #fff; font-size: 0.9rem; margin-bottom: 12px; }
        .token-input:focus { outline: none; border-color: #4cd8b5; }
        .submit-btn { width: 100%; padding: 14px; background: linear-gradient(135deg, #64ffda, #4cd8b5); border: none; border-radius: 12px; font-size: 1rem; font-weight: bold; color: #0a192f; cursor: pointer; }
        .info-cards { display: flex; gap: 12px; padding: 16px; overflow-x: auto; }
        .info-card { background: #112240; border-radius: 16px; padding: 12px 16px; min-width: 140px; border: 1px solid #64ffda; }
        .info-label { font-size: 0.7rem; color: #64ffda; text-transform: uppercase; }
        .info-value { font-size: 0.9rem; font-weight: bold; margin-top: 4px; }
        .action-buttons { display: flex; gap: 12px; padding: 0 16px 16px 16px; }
        .action-btn { flex: 1; padding: 12px; border: none; border-radius: 40px; font-weight: bold; font-size: 0.85rem; cursor: pointer; }
        .btn-clothes { background: #2e7d32; color: white; }
        .btn-loadout { background: #1565c0; color: white; }
        .btn-all { background: #64ffda; color: #0a192f; }
        .category-tabs { display: flex; gap: 8px; padding: 12px 16px; overflow-x: auto; background: #0a192f; border-bottom: 1px solid #64ffda; }
        .category-tab { padding: 8px 16px; background: #112240; border-radius: 40px; font-size: 0.85rem; white-space: nowrap; cursor: pointer; border: 1px solid #64ffda; }
        .category-tab.active { background: #64ffda; color: #0a192f; font-weight: bold; }
        .search-bar { padding: 12px 16px; background: #0a192f; display: flex; gap: 8px; flex-wrap: wrap; }
        .search-input { flex: 2; padding: 12px; background: #112240; border: 1px solid #64ffda; border-radius: 40px; color: #e6f1ff; font-size: 0.9rem; }
        .filter-select { flex: 1; padding: 12px; background: #112240; border: 1px solid #64ffda; border-radius: 40px; color: #e6f1ff; font-size: 0.85rem; }
        .items-container { padding: 16px; }
        .category-section { margin-bottom: 24px; }
        .category-header { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; padding: 0 4px; }
        .category-icon { font-size: 1.5rem; }
        .category-title { font-size: 1.1rem; font-weight: bold; color: #64ffda; }
        .category-count { font-size: 0.7rem; background: #1e3a5f; padding: 2px 8px; border-radius: 20px; }
        
        /* FIXED GRID - 3 COLUMNS ON PHONE */
        .item-grid { 
            display: grid; 
            gap: 12px; 
            grid-template-columns: repeat(3, 1fr);
        }
        
        .item-card { 
            background: #112240; 
            border-radius: 12px; 
            padding: 10px; 
            text-align: center; 
            cursor: pointer; 
            border: 2px solid transparent; 
            transition: all 0.2s;
        }
        .item-card.selected { border-color: #64ffda; background: #1e3a5f; }
        .item-card:active { transform: scale(0.97); }
        .item-card img { width: 100%; max-width: 70px; height: auto; object-fit: contain; border-radius: 8px; margin: 0 auto; display: block; }
        .item-name { font-size: 0.7rem; font-weight: 500; margin-top: 8px; overflow: hidden; text-overflow: ellipsis; color: #e6f1ff; word-break: break-word; white-space: normal; }
        .item-id { font-size: 0.55rem; color: #8892b0; margin-top: 4px; }
        .rarity-badge { display: inline-block; font-size: 0.55rem; background: rgba(0,0,0,0.6); padding: 2px 6px; border-radius: 20px; color: #64ffda; margin-top: 4px; }
        .keep-current { background: #1e3a5f; border-style: dashed; border-color: #64ffda; }
        .toast { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); padding: 12px 24px; border-radius: 40px; font-size: 0.85rem; font-weight: bold; z-index: 1000; animation: slideUp 0.3s ease; white-space: nowrap; }
        .toast.success { background: #2e7d32; color: white; }
        .toast.error { background: #c62828; color: white; }
        .toast.info { background: #64ffda; color: #0a192f; }
        @keyframes slideUp { from { opacity: 0; transform: translateX(-50%) translateY(20px); } to { opacity: 1; transform: translateX(-50%) translateY(0); } }
        .hidden { display: none; }
        .no-results { text-align: center; padding: 40px; color: #8892b0; }
        
        /* Tablet: 5 columns */
        @media (min-width: 600px) and (max-width: 899px) {
            .item-grid { grid-template-columns: repeat(5, 1fr); }
        }
        
        /* Desktop: 7 columns */
        @media (min-width: 900px) {
            .item-grid { grid-template-columns: repeat(7, 1fr); }
        }
        
        /* Small phone: 2 columns */
        @media (max-width: 400px) {
            .item-grid { grid-template-columns: repeat(2, 1fr); }
        }
    </style>
</head>
<body>
    <div class="header"><h1><span>🎮</span> FF Wardrobe</h1></div>
    
    {% if not loaded %}
    <div class="token-section">
        <form method="post">
            <input type="text" name="access_token" class="token-input" placeholder="Enter Access Token" required>
            <button type="submit" class="submit-btn">🔓 Load My Items</button>
        </form>
        <p style="font-size: 0.7rem; text-align: center; margin-top: 12px; color: #8892b0;">Access Token from Garena login</p>
    </div>
    {% else %}
    
    <div class="info-cards">
        <div class="info-card"><div class="info-label">👤 CHARACTER</div><div class="info-value">{{ current_character_name }}</div></div>
        <div class="info-card"><div class="info-label">🐾 PET</div><div class="info-value">{{ current_pet_name }}</div></div>
        <div class="info-card"><div class="info-label">📦 ITEMS</div><div class="info-value">{{ total_items }} owned</div></div>
    </div>
    
    <div class="action-buttons">
        <button class="action-btn btn-clothes" id="applyClothesBtn">👕 Apply Clothes</button>
        <button class="action-btn btn-loadout" id="applyLoadoutBtn">⚡ Apply Loadout</button>
        <button class="action-btn btn-all" id="applyAllBtn">✨ Apply All</button>
    </div>
    
    <div class="category-tabs" id="categoryTabs">
        <div class="category-tab active" data-category="clothes">👔 Clothes</div>
        <div class="category-tab" data-category="characters">👤 Characters</div>
        <div class="category-tab" data-category="pets">🐾 Pets</div>
    </div>
    
    <div class="search-bar">
        <input type="text" id="searchInput" class="search-input" placeholder="🔍 Search by name or ID...">
        <select id="slotFilter" class="filter-select"><option value="all">All Slots</option><option value="Mask">😷 Mask</option><option value="Top">👕 Top</option><option value="Bottom">👖 Bottom</option><option value="Shoes">👟 Shoes</option><option value="Head">🎭 Head</option></select>
        <select id="rarityFilter" class="filter-select"><option value="all">All Rarity</option><option value="EPIC">⭐ EPIC</option><option value="LEGENDARY">🔥 LEGENDARY</option><option value="MYTHIC">💎 MYTHIC</option></select>
    </div>
    
    <div class="items-container" id="itemsContainer">
        <div id="clothesSection" class="category-section">
            {% for slot in slots %}
            <div class="category-header" data-slot="{{ slot }}"><span class="category-icon">{{ slot_icons[slot] }}</span><span class="category-title">{{ slot }}</span><span class="category-count" id="count-{{ slot }}">0</span></div>
            <div class="item-grid" id="grid-{{ slot }}" data-slot="{{ slot }}"></div>
            {% endfor %}
        </div>
        <div id="charactersSection" class="category-section hidden"><div class="category-header"><span class="category-icon">👤</span><span class="category-title">Characters</span><span class="category-count" id="count-characters">0</span></div><div class="item-grid" id="grid-characters"></div></div>
        <div id="petsSection" class="category-section hidden"><div class="category-header"><span class="category-icon">🐾</span><span class="category-title">Pets</span><span class="category-count" id="count-pets">0</span></div><div class="item-grid" id="grid-pets"></div></div>
    </div>
    
    <div id="toast" class="toast" style="display: none;"></div>
    
    <script>
        const slotOrder = {{ slots | tojson }};
        const groupedData = {{ grouped | tojson }};
        const charactersData = {{ characters | tojson }};
        const petsData = {{ pets | tojson }};
        const equippedData = {{ equipped | tojson }};
        const currentCharacterId = {{ current_character_id }};
        const currentPetId = {{ current_pet_id }};
        const avatarId = {{ avatar_id }};
        
        let clothesSelections = {};
        let selectedCharacter = currentCharacterId;
        let selectedPet = currentPetId;
        let currentTab = 'clothes';
        let searchTerm = '';
        let slotFilter = 'all';
        let rarityFilter = 'all';
        
        slotOrder.forEach(slot => { clothesSelections[slot] = equippedData[slot] || null; });
        
        function showToast(message, type) {
            const toast = document.getElementById('toast');
            toast.textContent = message;
            toast.className = `toast ${type}`;
            toast.style.display = 'block';
            setTimeout(() => toast.style.display = 'none', 3000);
        }
        
        function filterItems(items) {
            return items.filter(item => {
                const matchesSearch = searchTerm === '' || item.name.toLowerCase().includes(searchTerm) || String(item.id).includes(searchTerm);
                let matchesRarity = rarityFilter === 'all';
                if (!matchesRarity && item.rare) matchesRarity = item.rare.toUpperCase() === rarityFilter;
                let matchesSlot = true;
                if (currentTab === 'clothes' && slotFilter !== 'all') matchesSlot = item.slot === slotFilter;
                return matchesSearch && matchesRarity && matchesSlot;
            });
        }
        
        function escapeHtml(text) { 
            const div = document.createElement('div'); 
            div.textContent = text; 
            return div.innerHTML; 
        }
        
        function renderClothes() {
            for (const slot of slotOrder) {
                const items = groupedData[slot] || [];
                const filteredItems = filterItems(items);
                const container = document.getElementById(`grid-${slot}`);
                const countSpan = document.getElementById(`count-${slot}`);
                if (!container) continue;
                countSpan.textContent = filteredItems.length;
                if (filteredItems.length === 0 && searchTerm !== '') { 
                    container.innerHTML = '<div class="no-results">No items found</div>'; 
                    continue; 
                }
                let html = '';
                const currentId = equippedData[slot];
                if (currentId && currentId !== 0) {
                    const isSelected = clothesSelections[slot] === currentId;
                    html += `<div class="item-card keep-current ${isSelected ? 'selected' : ''}" data-id="${currentId}" data-slot="${slot}" data-type="keep">
                        <img src="https://cdn.jsdelivr.net/gh/ShahGCreator/icon@main/PNG/${currentId}.png" onerror="this.src='https://via.placeholder.com/70?text=Current'">
                        <div class="item-name">Keep Current</div>
                        <div class="item-id">ID: ${currentId}</div>
                    </div>`;
                }
                for (const item of filteredItems) {
                    const isSelected = clothesSelections[slot] === item.id;
                    html += `<div class="item-card ${isSelected ? 'selected' : ''}" data-id="${item.id}" data-slot="${slot}" data-type="clothes">
                        <img src="https://cdn.jsdelivr.net/gh/ShahGCreator/icon@main/PNG/${item.id}.png" onerror="this.src='https://via.placeholder.com/70?text=No+Icon'">
                        <div class="item-name">${escapeHtml(item.name)}</div>
                        <div class="item-id">ID: ${item.id}</div>
                        ${item.rare ? `<div class="rarity-badge">⭐ ${item.rare}</div>` : ''}
                    </div>`;
                }
                container.innerHTML = html;
            }
            attachClothesEvents();
        }
        
        function renderCharacters() {
            const filteredItems = filterItems(charactersData);
            const container = document.getElementById('grid-characters');
            const countSpan = document.getElementById('count-characters');
            countSpan.textContent = filteredItems.length;
            if (filteredItems.length === 0 && searchTerm !== '') { 
                container.innerHTML = '<div class="no-results">No characters found</div>'; 
                return; 
            }
            let html = '';
            for (const item of filteredItems) {
                const isSelected = selectedCharacter === item.id;
                html += `<div class="item-card ${isSelected ? 'selected' : ''}" data-id="${item.id}" data-type="character">
                    <img src="https://cdn.jsdelivr.net/gh/ShahGCreator/icon@main/PNG/${item.id}.png" onerror="this.src='https://via.placeholder.com/70?text=No+Icon'">
                    <div class="item-name">${escapeHtml(item.name)}</div>
                    <div class="item-id">ID: ${item.id}</div>
                    ${item.rare ? `<div class="rarity-badge">⭐ ${item.rare}</div>` : ''}
                </div>`;
            }
            container.innerHTML = html;
            attachCharacterEvents();
        }
        
        function renderPets() {
            const filteredItems = filterItems(petsData);
            const container = document.getElementById('grid-pets');
            const countSpan = document.getElementById('count-pets');
            countSpan.textContent = filteredItems.length;
            if (filteredItems.length === 0 && searchTerm !== '') { 
                container.innerHTML = '<div class="no-results">No pets found</div>'; 
                return; 
            }
            let html = '';
            for (const item of filteredItems) {
                const isSelected = selectedPet === item.id;
                html += `<div class="item-card ${isSelected ? 'selected' : ''}" data-id="${item.id}" data-type="pet">
                    <img src="https://cdn.jsdelivr.net/gh/ShahGCreator/icon@main/PNG/${item.id}.png" onerror="this.src='https://via.placeholder.com/70?text=No+Icon'">
                    <div class="item-name">${escapeHtml(item.name)}</div>
                    <div class="item-id">ID: ${item.id}</div>
                    ${item.rare ? `<div class="rarity-badge">⭐ ${item.rare}</div>` : ''}
                </div>`;
            }
            container.innerHTML = html;
            attachPetEvents();
        }
        
        function attachClothesEvents() {
            document.querySelectorAll('.item-card[data-type="clothes"], .item-card[data-type="keep"]').forEach(card => {
                card.addEventListener('click', () => {
                    const id = parseInt(card.dataset.id);
                    const slot = card.dataset.slot;
                    if (clothesSelections[slot] === id) clothesSelections[slot] = null;
                    else clothesSelections[slot] = id;
                    renderClothes();
                });
            });
        }
        
        function attachCharacterEvents() {
            document.querySelectorAll('.item-card[data-type="character"]').forEach(card => {
                card.addEventListener('click', () => { 
                    selectedCharacter = parseInt(card.dataset.id); 
                    renderCharacters(); 
                });
            });
        }
        
        function attachPetEvents() {
            document.querySelectorAll('.item-card[data-type="pet"]').forEach(card => {
                card.addEventListener('click', () => { 
                    selectedPet = parseInt(card.dataset.id); 
                    renderPets(); 
                });
            });
        }
        
        function switchTab(tab) {
            currentTab = tab;
            document.querySelectorAll('.category-tab').forEach(t => {
                t.classList.toggle('active', t.dataset.category === tab);
            });
            const clothesSection = document.getElementById('clothesSection');
            const charactersSection = document.getElementById('charactersSection');
            const petsSection = document.getElementById('petsSection');
            if (tab === 'clothes') { 
                clothesSection.classList.remove('hidden'); 
                charactersSection.classList.add('hidden'); 
                petsSection.classList.add('hidden'); 
                renderClothes(); 
            } else if (tab === 'characters') { 
                clothesSection.classList.add('hidden'); 
                charactersSection.classList.remove('hidden'); 
                petsSection.classList.add('hidden'); 
                renderCharacters(); 
            } else if (tab === 'pets') { 
                clothesSection.classList.add('hidden'); 
                charactersSection.classList.add('hidden'); 
                petsSection.classList.remove('hidden'); 
                renderPets(); 
            }
        }
        
        async function applyClothes() {
            const skillIds = slotOrder.map(slot => { 
                const selected = clothesSelections[slot]; 
                return (selected === null || selected === undefined) ? (equippedData[slot] || 0) : selected; 
            });
            showToast('Applying clothes...', 'info');
            try {
                const response = await fetch('/apply_clothes', { 
                    method: 'POST', 
                    headers: { 'Content-Type': 'application/json' }, 
                    body: JSON.stringify({ avatar_id: avatarId, skill_ids: skillIds }) 
                });
                const data = await response.json();
                showToast(data.success ? '✓ Clothes changed!' : '✗ Error: ' + data.error, data.success ? 'success' : 'error');
            } catch (err) { 
                showToast('✗ Network error', 'error'); 
            }
        }
        
        async function applyLoadout() {
            showToast('Applying loadout...', 'info');
            try {
                const response = await fetch('/apply_loadout', { 
                    method: 'POST', 
                    headers: { 'Content-Type': 'application/json' }, 
                    body: JSON.stringify({ character_id: selectedCharacter }) 
                });
                const data = await response.json();
                showToast(data.success ? '✓ Loadout applied!' : '✗ Error: ' + data.error, data.success ? 'success' : 'error');
            } catch (err) { 
                showToast('✗ Network error', 'error'); 
            }
        }
        
        async function applyAll() { 
            await applyClothes(); 
            setTimeout(() => applyLoadout(), 1000); 
        }
        
        document.getElementById('applyClothesBtn').addEventListener('click', applyClothes);
        document.getElementById('applyLoadoutBtn').addEventListener('click', applyLoadout);
        document.getElementById('applyAllBtn').addEventListener('click', applyAll);
        document.getElementById('searchInput').addEventListener('input', (e) => { 
            searchTerm = e.target.value.toLowerCase(); 
            if (currentTab === 'clothes') renderClothes(); 
            else if (currentTab === 'characters') renderCharacters(); 
            else renderPets(); 
        });
        document.getElementById('slotFilter').addEventListener('change', (e) => { 
            slotFilter = e.target.value; 
            if (currentTab === 'clothes') renderClothes(); 
        });
        document.getElementById('rarityFilter').addEventListener('change', (e) => { 
            rarityFilter = e.target.value; 
            if (currentTab === 'clothes') renderClothes(); 
            else if (currentTab === 'characters') renderCharacters(); 
            else renderPets(); 
        });
        document.querySelectorAll('.category-tab').forEach(tab => tab.addEventListener('click', () => switchTab(tab.dataset.category)));
        
        renderClothes();
    </script>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        access_token = request.form.get('access_token', '').strip()
        if not access_token:
            return "Access token is required", 400
        
        jwt_token, err = get_jwt_from_access_token(access_token)
        if err:
            return f"Error converting token: {err}", 400
        
        try:
            payload_b64 = jwt_token.split('.')[1]
            payload_b64 += '=' * (4 - len(payload_b64) % 4)
            payload_json = base64.b64decode(payload_b64).decode('utf-8')
            payload = json.loads(payload_json)
            uid = payload.get('account_id')
        except Exception as e:
            return f"Error decoding token: {e}", 400

        char_id, equipped_items, pet_id, loadout, err = fetch_character_and_equipped(jwt_token, uid)
        if err:
            return f"Error fetching character info: {err}", 400

        item_ids, err = fetch_vault(jwt_token)
        if err:
            return f"Error fetching vault: {err}", 400

        item_map = load_item_database()
        
        grouped = defaultdict(list)
        characters = []
        pets = []
        
        for iid in item_ids:
            info = item_map.get(iid, {})
            item_type = info.get('type', 'Unknown')
            
            if item_type == 'Characters':
                characters.append({'id': iid, 'name': info.get('name', 'Unknown'), 'rare': info.get('Rare', '')})
            elif item_type == 'Pets':
                pets.append({'id': iid, 'name': info.get('name', 'Unknown'), 'rare': info.get('Rare', '')})
            else:
                slot = TYPE_TO_SLOT.get(item_type)
                if slot and slot in SLOT_ORDER:
                    grouped[slot].append({'id': iid, 'name': info.get('name', 'Unknown'), 'rare': info.get('Rare', ''), 'slot': slot})
        
        for slot in grouped:
            grouped[slot].sort(key=lambda x: x['name'])
        characters.sort(key=lambda x: x['name'])
        pets.sort(key=lambda x: x['name'])
        
        current_character_name = "Unknown"
        current_pet_name = "Unknown"
        if char_id in item_map:
            current_character_name = item_map[char_id].get('name', 'Unknown')
        if pet_id and pet_id in item_map:
            current_pet_name = item_map[pet_id].get('name', 'Unknown')
        
        session['token'] = jwt_token
        session['avatar_id'] = char_id

        return render_template_string(HTML_TEMPLATE,
                                      loaded=True,
                                      avatar_id=char_id,
                                      current_character_id=char_id,
                                      current_pet_id=pet_id or 0,
                                      current_character_name=current_character_name,
                                      current_pet_name=current_pet_name,
                                      grouped=dict(grouped),
                                      slots=SLOT_ORDER,
                                      slot_icons=SLOT_ICONS,
                                      equipped=equipped_items,
                                      characters=characters,
                                      pets=pets,
                                      total_items=len(item_ids))
    else:
        return render_template_string(HTML_TEMPLATE, loaded=False)

@app.route('/apply_clothes', methods=['POST'])
def apply_clothes():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data'}), 400
        avatar_id = data.get('avatar_id')
        skill_ids = data.get('skill_ids')
        if not avatar_id or not skill_ids or len(skill_ids) != 5:
            return jsonify({'success': False, 'error': 'Invalid input'}), 400

        token = session.get('token')
        if not token:
            return jsonify({'success': False, 'error': 'No token in session'}), 400

        success, err = apply_change_clothes(token, avatar_id, skill_ids)
        return jsonify({'success': success, 'error': err})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/apply_loadout', methods=['POST'])
def apply_loadout():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data'}), 400
        character_id = data.get('character_id')
        if not character_id:
            return jsonify({'success': False, 'error': 'Missing character_id'}), 400

        token = session.get('token')
        if not token:
            return jsonify({'success': False, 'error': 'No token in session'}), 400

        success, err = apply_select_loadout(token, character_id)
        return jsonify({'success': success, 'error': err})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🔥 Free Fire Wardrobe Manager - FIXED GRID 🔥")
    print("=" * 60)
    print("📱 Phone: 3 columns | Tablet: 5 columns | Desktop: 7 columns")
    print("🎨 Theme: Blue/Green")
    print("🌐 Server: http://localhost:5000")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)