from random import choice, randint
from time import time
from uuid import uuid4
from os import getcwd
from mmh3 import hash128
from hashlib import md5
from json import dumps

class fingerprint:

    def __init__(self, ipInfo: dict, challengeInfo: dict, browserInfo: dict) -> None:
        self.ipInfo = ipInfo
        self.challengeInfo = challengeInfo
        self.browserInfo = browserInfo
        self.userAgent = self.browserInfo["User-Agent"]
        self.language = self.ipInfo["language"]
        self.languages = self.ipInfo["languages"]
        self.timezoneOffset = self.ipInfo["timezoneOffset"]
        self.screenRes = [667, 375]
        self.speechVoice = self.getSpeechVoice()

    def hashBinary(self, string: str) -> str:
        return md5(string.encode("utf-8")).hexdigest()

    def x64hash128(self, t: str, r: int) -> str:
        o = hash128(t, r)
        return str(hex(((o & 0xffffffffffffffff) << 64) + (o >> 64))).removeprefix("0x")
    
    def getWebglHash(self, enhancedFp: dict) -> str:
        webglValues = {}
        for key, value in enhancedFp.items():
            if key.startswith("webgl_"):
                webglValues[key] = value
        return self.x64hash128(",".join([item for pair in webglValues.items() for item in pair]), 0)

    def getScreenResolution(self) -> list:
        resolutions = [
            [1920, 1080],
            [1920, 1200],
            [2048, 1080],
            [2560, 1440]
        ]

        return choice(resolutions)
    
    def getHardwareConcurrency(self) -> int:
        return choice([4, 8, 12, 16, 20])
    
    def getCfpUnmaskedRenderer(self) -> str:
        with open(f"{getcwd()}/fingerprints/cfpUnmaskedRenderers.txt", "r") as file:
            cfpUnmaskedRenderers = file.readlines()

        return choice(cfpUnmaskedRenderers).strip("\n").split(":")
    
    def getSpeechVoice(self) -> str:
        speechVoices = [
            "Microsoft Aria Online (Natural) - English (United States) || en-US",
            "Microsoft Ana Online (Natural) - English (United States) || en-US",
            "Microsoft Christopher Online (Natural) - English (United States) || en-US",
            "Microsoft Eric Online (Natural) - English (United States) || en-US",
            "Microsoft Guy Online (Natural) - English (United States) || en-US",
            "Microsoft Jenny Online (Natural) - English (United States) || en-US",
            "Microsoft Michelle Online (Natural) - English (United States) || en-US",
            "Microsoft Roger Online (Natural) - English (United States) || en-US",
            "Microsoft Steffan Online (Natural) - English (United States) || en-US"
        ]

        return choice(speechVoices)
    
    def getMediaDevices(self) -> list:
        types = ["audioinput", "audiooutput", "videoinput", "videooutput"]
        supportedDevices = []
 
        for _ in range(randint(1, 4)):
            randomType = choice(types)
            types.remove(randomType)
            
            supportedDevices.append({"kind": randomType, "id": "", "group": ""})
        
        supportedDevices = dumps(supportedDevices, separators=(',', ':'))
        mediaDevicesHash = self.hashBinary(supportedDevices)

        return [supportedDevices, mediaDevicesHash]

    def getFe(self) -> dict:
        fe = {
            "DNT": "unknown",
            "L": self.language,
            "D": 32,
            "PR": 2,
            "S": self.screenRes,
            "AS": self.screenRes,
            "TO": self.timezoneOffset,
            "SS": True,
            "LS": True,
            "IDB": True,
            "B": False,
            "ODB": False,
            "CPUC": "unknown",
            "PK": "iPhone",
            "CFP": "2088793484",
            "FR": False,
            "FOS": False,
            "FB": False,
            "JSF": "Arial,Arial Hebrew,Arial Rounded MT Bold,Courier,Courier New,Georgia,Helvetica,Helvetica Neue,Palatino,Times,Times New Roman,Trebuchet MS,Verdana",
            "P": "",
            "T": [5, True, True],
            "H": choice([2, 4]),
            "SWF": False
        }

        fe["S"] = ','.join(map(str, fe["S"]))
        fe["AS"] = ','.join(map(str, fe["AS"]))
        fe["T"] = ','.join(map(str, fe["T"]))

        return fe
    
    def getEnhancedFp(self) -> dict:
        enhancedFp = {
            'webgl_extensions': 'EXT_blend_minmax;EXT_sRGB;EXT_frag_depth;OES_texture_float;OES_texture_float_linear;OES_texture_half_float;OES_texture_half_float_linear;OES_standard_derivatives;EXT_shader_texture_lod;EXT_texture_filter_anisotropic;OES_vertex_array_object;OES_element_index_uint;OES_fbo_render_mipmap;WEBGL_lose_context;WEBGL_compressed_texture_astc;WEBGL_compressed_texture_etc;WEBGL_compressed_texture_etc1;WEBKIT_WEBGL_compressed_texture_pvrtc;WEBGL_compressed_texture_pvrtc;WEBGL_depth_texture;WEBGL_draw_buffers;ANGLE_instanced_arrays;WEBGL_debug_shaders;WEBGL_debug_renderer_info;EXT_color_buffer_half_float;WEBGL_color_buffer_float;KHR_parallel_shader_compile;WEBGL_multi_draw',
            'webgl_extensions_hash': '25d15597e2882cd15da8d4cb9314398c',
            'webgl_renderer': 'WebKit WebGL',
            'webgl_vendor': 'WebKit',
            'webgl_version': 'WebGL 1.0',
            'webgl_shading_language_version': 'WebGL GLSL ES 1.0 (1.0)',
            'webgl_aliased_line_width_range': '[1, 1]',
            'webgl_aliased_point_size_range': '[1, 511]',
            'webgl_antialiasing': 'yes',
            'webgl_bits': '8,8,24,8,8,0',
            'webgl_max_params': '16,32,16384,1024,16384,16,16384,31,16,16,1024',
            'webgl_max_viewport_dims': '[16384, 16384]',
            'webgl_unmasked_vendor': "Apple Inc.",
            'webgl_unmasked_renderer': "Apple GPU",
            'webgl_vsf_params': '23,127,127,23,127,127,23,127,127',
            'webgl_vsi_params': '0,31,30,0,31,30,0,31,30',
            'webgl_fsf_params': '23,127,127,23,127,127,23,127,127',
            'webgl_fsi_params': '0,31,30,0,31,30,0,31,30',
            'webgl_hash_webgl': "",
            'user_agent_data_brands': None,
            'user_agent_data_mobile': None,
            'navigator_connection_downlink': None,
            'navigator_connection_downlink_max': None,
            'network_info_rtt': None,
            'network_info_save_data': None,
            'network_info_rtt_type': None,
            'screen_pixel_depth': 32,
            'navigator_device_memory': None,
            'navigator_pdf_viewer_enabled': None,
            'navigator_languages': self.languages,
            'window_inner_width': 0,
            'window_inner_height': 0,
            'window_outer_width': self.screenRes[1],
            'window_outer_height': self.screenRes[0],
            'browser_detection_firefox': False,
            'browser_detection_brave': False,
            'browser_api_checks': [
                "permission_status: false",
                "eye_dropper: false",
                "audio_data: false",
                "writable_stream: true",
                "css_style_rule: false",
                "navigator_ua: false",
                "barcode_detector: false",
                "display_names: true",
                "contacts_manager: false",
                "svg_discard_element: false",
                "usb: NA",
                "media_device: defined",
                "playback_quality: true"
            ],
            'browser_object_checks': None,
            '29s83ih9': "68934a3e9455fa72420237eb05902327⁣",
            'audio_codecs': '{\\"ogg\\":\\"\\",\\"mp3\\":\\"maybe\\",\\"wav\\":\\"\\",\\"m4a\\":\\"maybe\\",\\"aac\\":\\"maybe\\"}',
            'audio_codecs_extended_hash': 'c92f8b3f8e3265ecf22129615cc46ea8',
            'video_codecs': '{\\"ogg\\":\\"\\",\\"h264\\":\\"probably\\",\\"webm\\":\\"\\",\\"mpeg4v\\":\\"probably\\",\\"mpeg4a\\":\\"probably\\",\\"theora\\":\\"\\"}',
            'video_codecs_extended_hash': '996d499199483186e5faed9dd3f648fb',
            'media_query_dark_mode': True,
            'css_media_queries': 0,
            'css_color_gamut': 'p3',
            'css_contrast': 'no-preference',
            'css_monochrome': False,
            'css_pointer': 'coarse',
            'css_grid_support': False,
            'headless_browser_phantom': False,
            'headless_browser_selenium': False,
            'headless_browser_nightmare_js': False,
            'headless_browser_generic': 4,
            '1l2l5234ar2': f"{int(time())}⁣",
            'document__referrer': self.challengeInfo["site"],
            'window__ancestor_origins': self.challengeInfo["ancestorOrigins"],
            'window__tree_index': self.challengeInfo["treeIndex"],
            'window__tree_structure': self.challengeInfo["treeStructure"],
            'window__location_href': f'{self.challengeInfo["surl"]}/v2/2.11.0/enforcement.5a3219a1826f6bf969b7a09159e9d637.html',
            'client_config__sitedata_location_href': self.challengeInfo["locationHref"],
            'client_config__language': self.language.lower() if self.challengeInfo["languageEnabled"] else None,
            'client_config__surl': self.challengeInfo["surl"],
            'c8480e29a': f'{self.hashBinary(self.challengeInfo["surl"])}⁢',
            'client_config__triggered_inline': False,
            'mobile_sdk__is_sdk': False,
            'audio_fingerprint': '124.0434485301812',
            'navigator_battery_charging': None,
            'media_device_kinds': [],
            'media_devices_hash': "d751713988987e9331980363e24189ce",
            'navigator_permissions_hash': None,
            'math_fingerprint': "e4889aec3d9e3cdc6602c187bc80a578",
            'supported_math_functions': "afad9aebfa1a08d54b39f540d0c002f1",
            'screen_orientation': None,
            'rtc_peer_connection': 1,
            '4b4b269e68': str(uuid4()),
            '6a62b2a558': '5a3219a1826f6bf969b7a09159e9d637',
            'speech_default_voice': self.speechVoice,
            'speech_voices_hash': ''.join(choice('0123456789abcdef') for _ in range(32)),
            '4ca87df3d1': 'Ow==',
            '867e25e5d4': 'Ow==',
            'd4a306884c': 'Ow=='
        }

        enhancedFp["webgl_hash_webgl"] = self.getWebglHash(enhancedFp)

        return enhancedFp