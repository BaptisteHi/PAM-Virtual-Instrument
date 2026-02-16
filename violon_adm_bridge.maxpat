{
    "patcher": {
        "fileversion": 1,
        "appversion": {
            "major": 9,
            "minor": 1,
            "revision": 2,
            "architecture": "x64",
            "modernui": 1
        },
        "classnamespace": "box",
        "rect": [ 34.0, 77.0, 1065.0, 705.0 ],
        "boxes": [
            {
                "box": {
                    "automatic": 1,
                    "id": "obj-18",
                    "maxclass": "scope~",
                    "numinlets": 2,
                    "numoutlets": 0,
                    "patching_rect": [ 493.75, 1096.875, 418.4615783691406, 166.15386199951172 ]
                }
            },
            {
                "box": {
                    "id": "obj-17",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 1490.908959388733, 1207.575651049614, 150.0, 20.0 ],
                    "text": "force au chevalet"
                }
            },
            {
                "box": {
                    "id": "obj-9",
                    "linecount": 2,
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 1483.4616870880127, 425.75753819942474, 153.0, 34.0 ],
                    "text": " vitesse au chevalet, filtrée par l'admittance"
                }
            },
            {
                "box": {
                    "automatic": 1,
                    "id": "obj-4",
                    "maxclass": "scope~",
                    "numinlets": 2,
                    "numoutlets": 0,
                    "patching_rect": [ 1050.0, 1117.7778310775757, 418.4615783691406, 166.15386199951172 ]
                }
            },
            {
                "box": {
                    "id": "obj-61",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 481.4814656972885, 352.8518403172493, 150.0, 20.0 ],
                    "text": "fixe"
                }
            },
            {
                "box": {
                    "id": "obj-60",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 455.6111190319061, 300.25924944877625, 150.0, 20.0 ],
                    "text": "variable"
                }
            },
            {
                "box": {
                    "id": "obj-59",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 431.11109697818756, 273.131139755249, 150.0, 20.0 ],
                    "text": "variable"
                }
            },
            {
                "box": {
                    "id": "obj-57",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 476.29628068208694, 327.6666559576988, 150.0, 20.0 ],
                    "text": "fixe"
                }
            },
            {
                "box": {
                    "id": "obj-55",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 519.1334669589996, 42.1875, 319.49153304100037, 20.0 ],
                    "text": "Paramètres modaux de l'admittance du chevalet"
                }
            },
            {
                "box": {
                    "id": "obj-49",
                    "linecount": 3,
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 840.625, 185.9375, 1844.0, 50.0 ],
                    "text": "Zmod 0.02806 0.030843 0.025089 0.016473 0.028986 0.053522 0.022354 0.017469 0.025486 0.006351 0.016635 0.013245 0.014157 0.003408 0.009902 0.017948 0.026973 0.00743 0.032272 0.005593 0.007634 0.007395 0.034328 0.009036 0.013227 0.01258 0.011989 0.011913 0.005868 0.007603 0.006733 0.014741 0.008533 0.009627 0.007925 0.017791 0.018195 0.005393 0.003666 0.00303 0.005134 0.066572 0.007576 0.002656 0.00493 0.004758 0.029097 0.006207 0.003136 0.005549 0.00449 0.003319 0.003433 0.005452 0.012034 0.004008 0.004949 0.003452 0.002172 0.002138 0.00364 0.006323 0.005444 0.003339 0.00347 0.003448 0.005739 0.007608 0.007751 0.001509 0.004041 0.008232 0.003168 0.002106 0.00273 0.002993 0.003488 0.00345 0.001683 0.011974 0.001215 0.002213 0.00152 0.003111 0.003052 0.002035 0.002587 0.003725"
                }
            },
            {
                "box": {
                    "id": "obj-44",
                    "linecount": 4,
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 840.625, 112.5, 1858.0, 64.0 ],
                    "text": "Wmod 1373.413794 1818.49807 2812.808638 3682.948216 3878.181447 4271.486041 5353.815038 5778.452768 6946.047352 7187.139422 7633.209517 8362.761828 8884.677319 9562.667766 10044.215276 10911.039688 11230.857653 11441.417113 12132.573726 12329.132521 12779.992896 13487.223907 13812.89152 14128.224227 14734.279208 15686.360266 15880.162351 16519.575117 17246.926539 17556.028167 18211.477956 18420.358618 19067.828992 19407.986363 19969.942067 20265.409703 21189.552273 21811.022133 22052.921262 22739.883354 23255.361525 23933.814837 25293.02, 26997.22 27480.728788 28010.973791 28637.81813 29501.527447 31153.131017 31742.551951 32169.769459 32771.098753 33295.552677 33810.294205 35528.244306 36290.785273 36707.915374 37180.081467 37698.751477 38266.068861 38776.017225 39247.374682 39615.878256 40181.062019 40721.609574 41287.404396 41826.767519 42272.72689 42645.797896 43529.879492 44303.782728 44545.695465 45024.020635 45610.722268 46183.958417 46667.217531 47233.867565 47764.67168 48355.050809 48456.698949 50110.583659 50580.270274 51108.591033 51660.137059 52053.125359 52573.242922 53042.473895 53780.579341"
                }
            },
            {
                "box": {
                    "id": "obj-20",
                    "linecount": 3,
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 840.625, 54.6875, 1851.0, 50.0 ],
                    "text": "Mmod 1.797487 0.304601 98.138926 0.02025 0.146994 0.128842 0.370522 0.265211 0.022144 0.042631 0.122402 0.062906 0.013751 1.618522 0.035819 0.382305 0.056474 0.722967 0.189861 0.04448 0.050795 0.030931 0.082283 0.034803 0.018117 0.031536 0.115636 0.010929 0.030999 0.314412 0.032312 0.009403 0.088533 0.060034 0.117536 0.017931 0.103311 1.693788 0.083812 0.258749 0.194356 0.012648 0.224812 0.930449 0.500597 1.075612 0.152485 6.3 0.276328 0.339845 0.852437 0.8739 5.341969 31.77886 0.241606 0.31575 0.873137 2.475329 2.380168 0.797399 0.553424 0.409067 0.280668 0.249392 0.196483 0.229334 0.191166 0.356257 0.371703 0.395963 1.013909 0.681652 3.706183 0.914413 0.310323 0.273507 0.275775 0.72018 1.213651 0.468824 1.727531 0.362915 0.259365 0.114876 0.175412 0.535972 1.668802 13.358735"
                }
            },
            {
                "box": {
                    "automatic": 1,
                    "id": "obj-2",
                    "maxclass": "scope~",
                    "numinlets": 2,
                    "numoutlets": 0,
                    "patching_rect": [ 1050.0, 273.0, 418.4615783691406, 166.15386199951172 ]
                }
            },
            {
                "box": {
                    "id": "obj-52",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "signal" ],
                    "patching_rect": [ 422.4138152599335, 910.3448753356934, 44.0, 22.0 ],
                    "text": "*~ 127"
                }
            },
            {
                "box": {
                    "id": "obj-53",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "signal" ],
                    "patching_rect": [ 422.4138152599335, 879.3103909492493, 33.0, 22.0 ],
                    "text": "+~ 1"
                }
            },
            {
                "box": {
                    "id": "obj-51",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "signal" ],
                    "patching_rect": [ 588.8888790607452, 898.2759091854095, 44.0, 22.0 ],
                    "text": "*~ 127"
                }
            },
            {
                "box": {
                    "id": "obj-50",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "signal" ],
                    "patching_rect": [ 588.8888790607452, 867.2414247989655, 33.0, 22.0 ],
                    "text": "+~ 1"
                }
            },
            {
                "box": {
                    "id": "obj-25",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "signal" ],
                    "patching_rect": [ 334.8852376937866, 909.8695442676544, 54.0, 22.0 ],
                    "text": "sig~ 255"
                }
            },
            {
                "box": {
                    "id": "obj-13",
                    "maxclass": "newobj",
                    "numinlets": 6,
                    "numoutlets": 1,
                    "outlettype": [ "signal" ],
                    "patching_rect": [ 588.8888790607452, 839.6552164554596, 98.0, 22.0 ],
                    "text": "scale~ -10 2 -1 1"
                }
            },
            {
                "box": {
                    "id": "obj-12",
                    "maxclass": "newobj",
                    "numinlets": 6,
                    "numoutlets": 1,
                    "outlettype": [ "signal" ],
                    "patching_rect": [ 422.4138152599335, 839.6552164554596, 98.0, 22.0 ],
                    "text": "scale~ -10 2 -1 1"
                }
            },
            {
                "box": {
                    "id": "obj-10",
                    "maxclass": "newobj",
                    "numinlets": 3,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 424.1111190319061, 983.8695468902588, 109.0, 22.0 ],
                    "text": "jit.poke~ scope 2 1"
                }
            },
            {
                "box": {
                    "id": "obj-3",
                    "maxclass": "live.scope~",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "bang" ],
                    "patching_rect": [ 1046.1539459228516, 467.6923522949219, 1024.6154823303223, 278.4615650177002 ],
                    "range": [ -4.0, 1.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-39",
                    "maxclass": "spectroscope~",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 1046.5517790317535, 774.1379716396332, 1024.0, 313.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-16",
                    "maxclass": "message",
                    "numinlets": 2,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "patching_rect": [ 53.4482786655426, 529.3103725910187, 35.0, 22.0 ],
                    "text": "reset"
                }
            },
            {
                "box": {
                    "id": "obj-15",
                    "maxclass": "button",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 511.1111190319061, 501.58730936050415, 24.0, 24.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-14",
                    "lastchannelcount": 0,
                    "maxclass": "live.gain~",
                    "numinlets": 2,
                    "numoutlets": 5,
                    "outlettype": [ "signal", "signal", "", "float", "list" ],
                    "parameter_enable": 1,
                    "patching_rect": [ 93.47825908660889, 778.2608547210693, 48.0, 136.0 ],
                    "saved_attribute_attributes": {
                        "valueof": {
                            "parameter_longname": "live.gain~",
                            "parameter_mmax": 6.0,
                            "parameter_mmin": -70.0,
                            "parameter_modmode": 3,
                            "parameter_shortname": "live.gain~",
                            "parameter_type": 0,
                            "parameter_unitstyle": 4
                        }
                    },
                    "varname": "live.gain~"
                }
            },
            {
                "box": {
                    "id": "obj-5",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "signal" ],
                    "patching_rect": [ 511.1111190319061, 538.0952464342117, 39.0, 22.0 ],
                    "text": "click~"
                }
            },
            {
                "box": {
                    "id": "obj-91",
                    "maxclass": "ezdac~",
                    "numinlets": 2,
                    "numoutlets": 0,
                    "patching_rect": [ 95.65217208862305, 960.8695468902588, 45.0, 45.0 ]
                }
            },
            {
                "box": {
                    "bubble": 1,
                    "fontname": "Arial",
                    "fontsize": 13.0,
                    "id": "obj-8",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 1766.666624546051, 365.7131042480469, 166.0, 25.0 ],
                    "text": "choose a sampling rate"
                }
            },
            {
                "box": {
                    "bubble": 1,
                    "fontname": "Arial",
                    "fontsize": 13.0,
                    "id": "obj-6",
                    "maxclass": "comment",
                    "numinlets": 1,
                    "numoutlets": 0,
                    "patching_rect": [ 1709.999959230423, 279.04643964767456, 195.245117, 25.0 ],
                    "text": "report sampling rate choices"
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 13.0,
                    "id": "obj-37",
                    "maxclass": "number",
                    "numinlets": 1,
                    "numoutlets": 2,
                    "outlettype": [ "", "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 1779.999957561493, 339.0464382171631, 55.0, 23.0 ],
                    "triangle": 0,
                    "triscale": 0.9
                }
            },
            {
                "box": {
                    "id": "obj-45",
                    "items": [ 11025, ",", 12000, ",", 16000, ",", 22050, ",", 24000, ",", 32000, ",", 44100, ",", 48000, ",", 88200, ",", 96000, ",", 192000 ],
                    "maxclass": "umenu",
                    "numinlets": 1,
                    "numoutlets": 3,
                    "outlettype": [ "int", "", "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 1689.9999597072601, 365.7131042480469, 78.0, 22.0 ]
                }
            },
            {
                "box": {
                    "id": "obj-46",
                    "maxclass": "button",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "bang" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 1689.9999597072601, 282.37977290153503, 20.0, 20.0 ]
                }
            },
            {
                "box": {
                    "fontname": "Arial",
                    "fontsize": 13.0,
                    "id": "obj-82",
                    "maxclass": "newobj",
                    "numinlets": 2,
                    "numoutlets": 2,
                    "outlettype": [ "", "int" ],
                    "patching_rect": [ 1689.9999597072601, 312.3797721862793, 110.0, 23.0 ],
                    "text": "adstatus sr"
                }
            },
            {
                "box": {
                    "id": "obj-76",
                    "maxclass": "newobj",
                    "numinlets": 1,
                    "numoutlets": 3,
                    "outlettype": [ "signal", "signal", "signal" ],
                    "patcher": {
                        "fileversion": 1,
                        "appversion": {
                            "major": 9,
                            "minor": 1,
                            "revision": 2,
                            "architecture": "x64",
                            "modernui": 1
                        },
                        "classnamespace": "dsp.gen",
                        "rect": [ 34.0, 77.0, 1468.0, 705.0 ],
                        "boxes": [
                            {
                                "box": {
                                    "id": "obj-14",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 1741.0, 1101.0, 35.0, 22.0 ],
                                    "text": "out 3"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-12",
                                    "maxclass": "newobj",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 1102.0, 557.7319275140762, 47.0, 22.0 ],
                                    "text": "r D_left"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-11",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 1585.0926415125527, 1124.0, 35.0, 22.0 ],
                                    "text": "out 2"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-9",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 1337.0, 610.0, 33.0, 22.0 ],
                                    "text": "* 0.5"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-10",
                                    "maxclass": "newobj",
                                    "numinlets": 2,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 1319.0, 658.0, 37.0, 22.0 ],
                                    "text": "delay"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-8",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 1102.0, 610.0, 33.0, 22.0 ],
                                    "text": "* 0.5"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-3",
                                    "maxclass": "newobj",
                                    "numinlets": 2,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 1084.0, 658.0, 37.0, 22.0 ],
                                    "text": "delay"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-98",
                                    "maxclass": "newobj",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 1716.9259877204895, 670.3703591823578, 29.0, 22.0 ],
                                    "text": "r Zc"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-97",
                                    "maxclass": "newobj",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 1497.6259645462037, 624.0, 55.0, 22.0 ],
                                    "text": "r D_right"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-96",
                                    "maxclass": "newobj",
                                    "numinlets": 2,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 1479.6259645462037, 665.0, 37.0, 22.0 ],
                                    "text": "delay"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-95",
                                    "maxclass": "newobj",
                                    "numinlets": 2,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 1400.5259568214417, 600.0, 47.0, 22.0 ],
                                    "text": "delay 2"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-94",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 1400.5259568214417, 503.7036952972412, 89.0, 22.0 ],
                                    "text": "history qtot_val"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-92",
                                    "maxclass": "newobj",
                                    "numinlets": 2,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 1242.0, 665.0, 47.0, 22.0 ],
                                    "text": "delay 2"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-91",
                                    "maxclass": "newobj",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 1181.0, 554.0, 47.0, 22.0 ],
                                    "text": "r D_left"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-90",
                                    "maxclass": "newobj",
                                    "numinlets": 2,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 1163.0, 600.0, 37.0, 22.0 ],
                                    "text": "delay"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-89",
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 1189.0, 489.0, 150.0, 20.0 ],
                                    "text": " q_o"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-87",
                                    "maxclass": "newobj",
                                    "numinlets": 2,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 1163.0, 455.0, 29.5, 22.0 ],
                                    "text": "+"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-86",
                                    "maxclass": "newobj",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 1263.0, 393.0, 56.0, 22.0 ],
                                    "text": "r Yc_half"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-85",
                                    "maxclass": "newobj",
                                    "numinlets": 2,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 1207.0, 422.0, 29.5, 22.0 ],
                                    "text": "*"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-84",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 1207.0, 366.0, 73.0, 22.0 ],
                                    "text": "history f_val"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-83",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 1085.0, 366.0, 94.0, 22.0 ],
                                    "text": "history q_iR_val"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-82",
                                    "maxclass": "newobj",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 1023.0259181976319, 557.7319275140762, 55.0, 22.0 ],
                                    "text": "r D_right"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-81",
                                    "maxclass": "newobj",
                                    "numinlets": 2,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 1005.0259181976319, 599.9999899864197, 37.0, 22.0 ],
                                    "text": "delay"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-79",
                                    "maxclass": "newobj",
                                    "numinlets": 2,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 937.0370213985443, 599.9999899864197, 47.0, 22.0 ],
                                    "text": "delay 2"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-78",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 937.0370213985443, 503.7036952972412, 92.0, 22.0 ],
                                    "text": "history q_iL_val"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-77",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 258.62884986400604, 503.0, 31.0, 22.0 ],
                                    "text": "s Zc"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-76",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 692.5385514497757, 503.0, 57.0, 22.0 ],
                                    "text": "s D_right"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-75",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 475.7949335177739, 503.0, 49.0, 22.0 ],
                                    "text": "s D_left"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-68",
                                    "maxclass": "newobj",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 1629.0370902485317, 670.3703591823578, 56.0, 22.0 ],
                                    "text": "r Yc_half"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-56",
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 15.384617328643799, 552.5641723871231, 150.0, 20.0 ],
                                    "text": "Paramètres de contrôle"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-53",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 42.30769765377045, 503.0, 58.0, 22.0 ],
                                    "text": "s Yc_half"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-43",
                                    "maxclass": "newobj",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 15.384617328643799, 130.7692472934723, 196.0, 22.0 ],
                                    "text": "param @default 0.00045 @name d"
                                }
                            },
                            {
                                "box": {
                                    "code": "R = d / 2;                                                  // rayon de la corde (m)\r\nc = sqrt(tension / mu);                                     // vitesse du son (m/s)\r\nT_left = 2*L*x/c;                                           // temps de parcours aller-retour de la partie gauche de la corde (s) \r\nT_right = 2*L*(1-x)/c;                                      // temps de parcours aller-retour de la partie droite de la corde (s)\r\nD_left = int(round(T_left*samplerate));\r\nD_right = int(round(T_right*samplerate));\r\narea = PI*R*R;                                              // section de la corde (m^2)\r\nrho = mu / area;                                            // masse volumique (kg/m^3)\r\nf0 = c / (2*L);                                             // fréquence fondamentale\r\nZc = rho * c * area;                                        // impédance caractéristique (kg/s)\r\nYc = 1 / Zc;                                                // admittance (s/kg)\r\nYc_half = Yc/2;\r\n\r\nout1=Yc_half; out2=Zc; out3=D_left; out4=D_right;",
                                    "fontface": 0,
                                    "fontname": "<Monospaced>",
                                    "fontsize": 12.0,
                                    "id": "obj-40",
                                    "maxclass": "codebox",
                                    "numinlets": 1,
                                    "numoutlets": 4,
                                    "outlettype": [ "", "", "", "" ],
                                    "patching_rect": [ 42.30769765377045, 289.7436263561249, 669.2308537960052, 192.30771660804749 ]
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-32",
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 46.1538519859314, 264.1025974750519, 150.0, 20.0 ],
                                    "text": "Paramètres dérivés"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-19",
                                    "maxclass": "newobj",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 15.384617328643799, 106.41026985645294, 206.0, 22.0 ],
                                    "text": "param @default 0.00072 @name mu"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-13",
                                    "maxclass": "comment",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 15.384617328643799, 37.333343863487244, 150.0, 20.0 ],
                                    "text": "Paramètres physiques"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-29",
                                    "maxclass": "newobj",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 737.0370247364044, 633.333322763443, 167.0, 22.0 ],
                                    "text": "in 1 @comment start_impulse"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-28",
                                    "maxclass": "newobj",
                                    "numinlets": 2,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 925.9259104728699, 674.0740628242493, 29.5, 22.0 ],
                                    "text": "+"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-15",
                                    "maxclass": "newobj",
                                    "numinlets": 1,
                                    "numoutlets": 0,
                                    "patching_rect": [ 1716.9259877204895, 1124.0, 35.0, 22.0 ],
                                    "text": "out 1"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-7",
                                    "maxclass": "newobj",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 15.384617328643799, 648.7180306911469, 355.0, 22.0 ],
                                    "text": "param @default 0.039 @min 0.001 @max 0.999 @name w_ratio"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-6",
                                    "maxclass": "newobj",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 15.384617328643799, 624.3590532541275, 309.0, 22.0 ],
                                    "text": "param @default 0.05 @min 0.0001 @max 1. @name v0"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-5",
                                    "maxclass": "newobj",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 15.384617328643799, 600.0000758171082, 297.0, 22.0 ],
                                    "text": "param @default 0.2 @min 0.001 @max 5. @name Fb"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-4",
                                    "maxclass": "newobj",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 15.384617328643799, 575.6410983800888, 309.0, 22.0 ],
                                    "text": "param @default 0.45 @min 0.001 @max 0.5 @name vb"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-38",
                                    "maxclass": "newobj",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 15.384617328643799, 83.33334386348724, 215.0, 22.0 ],
                                    "text": "param @default 58.86 @name tension"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-37",
                                    "maxclass": "newobj",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 15.384617328643799, 672.7180306911469, 322.0, 22.0 ],
                                    "text": "param @default 0.31255 @min 0.01 @max 0.99 @name x"
                                }
                            },
                            {
                                "box": {
                                    "id": "obj-36",
                                    "maxclass": "newobj",
                                    "numinlets": 0,
                                    "numoutlets": 1,
                                    "outlettype": [ "" ],
                                    "patching_rect": [ 15.384617328643799, 59.333343863487244, 303.0, 22.0 ],
                                    "text": "param @default 0.325 @min 0.01 @max 0.7 @name L"
                                }
                            },
                            {
                                "box": {
                                    "code": "// Fonction get_q_and_f --> otenir q(t) et f(q) à partir de q(h)\r\n\r\nF_continu(q_, vb_, Fb_, v0_){\r\n    frac = (vb_ - q_) / v0_;\r\n    return Fb_ * frac  / (1 + frac*frac);   \r\n}\r\n\r\ndicho(q_, q_h_, Yc_half_, vb_, Fb_, v0_) {\r\n    return q_ - q_h_ - Yc_half_ * F_continu(q_, vb_, Fb_, v0_);\r\n}\r\n\r\nprime_dicho(q_, q_h_, Yc_half_, vb_, Fb_, v0_) {\r\n    frac = (vb_ - q_) / v0_;\r\n    df_dq = - (Fb_ / v0_) * (1 - frac*frac) / ((1 + frac*frac)*(1 + frac*frac));\r\n    return 1.0 - Yc_half_ * df_dq;\r\n}\r\n\r\n\r\nHistory q_guess(0);\r\nHistory init(0);\r\nHistory initialized(0);\r\nHistory fb_prev1(0);\r\nHistory fb_prev2(0);\r\nData Mmod(88);\r\nData Wmod(88);\r\nData Zmod(88);\r\nData gm(88);\r\nData fm(88);\r\nData fm_prev(88);\r\nData fm_prev2(88);\r\nData wm(88);\r\nData wm_prev(88);\r\nData wm_prev2(88);\r\nData a_m0(88);\r\nData a_m1(88);\r\nData a_m2(88);\r\nData bm(88);\r\n\r\nqiL_prev2 = in1;\r\nqiL_D = in2;\r\nqiL_halfD = in3;\r\nqo_D = 0.995*in4;\r\nqo_D2 = 0.995*in5;\r\nqo_halfD = in6;\r\nqtot_prev2 = in7;\r\nf_D = in8;\r\nYc_half = in9;\r\nZc = in10;\r\n\r\n\r\n\ndt = 1 / samplerate;\n\n// On ne calcule ces 88 coefficients qu'une seule fois\nif (initialized == 0) {\r\n    poke(Mmod, 1.797487, 0);\r\n    poke(Mmod,  0.304601, 1);\r\n    poke(Mmod, 98.138926, 2);\r\n    poke(Mmod, 0.02025, 3);\r\n    poke(Mmod, 0.146994, 4);\r\n    poke(Mmod, 0.128842, 5);\r\n    poke(Mmod, 0.370522, 7);\r\n    poke(Mmod, 0.265211, 8);\r\n    poke(Mmod, 0.022144, 9);\r\n    poke(Mmod, 0.042631, 10);\r\n    poke(Mmod, 0.122402, 11);\r\n    poke(Mmod, 0.062906, 12);\r\n    poke(Mmod, 0.013751, 13);\r\n    poke(Mmod, 1.618522, 14);\r\n    poke(Mmod, 0.035819, 15);\r\n    poke(Mmod, 0.382305, 16);\r\n    poke(Mmod, 0.056474, 17);\r\n    poke(Mmod, 0.722967, 18);\r\n    poke(Mmod, 0.189861, 19);\r\n    poke(Mmod, 0.04448, 20);\r\n    poke(Mmod,  0.050795, 21);\r\n    poke(Mmod, 0.030931, 22);\r\n    poke(Mmod, 0.082283, 23);\r\n    poke(Mmod, 0.034803, 24);\r\n    poke(Mmod, 0.018117, 25);\r\n    poke(Mmod, 0.031536, 26);\r\n    poke(Mmod, 0.115636, 27);\r\n    poke(Mmod, 0.010929, 28);\r\n    poke(Mmod, 0.030999, 29);\r\n    poke(Mmod, 0.314412, 30);\r\n    poke(Mmod, 0.032312, 31);\r\n    poke(Mmod, 0.009403, 32);\r\n    poke(Mmod, 0.088533, 33);\r\n    poke(Mmod, 0.060034, 34);\r\n    \r\n    poke(Wmod, 1373.413794, 0);\r\n    poke(Wmod, 1818.49807, 1);\r\n    poke(Wmod, 2812.808638, 2);\r\n    poke(Wmod, 3682.948216, 3);\r\n    poke(Wmod, 3878.181447, 4);\r\n    poke(Wmod, 4271.486041, 5);\r\n    poke(Wmod, 5353.815038, 6);\r\n    poke(Wmod, 5778.452768, 7);\r\n    poke(Wmod, 6946.047352, 8);\r\n    poke(Wmod, 7187.139422, 9);\r\n    poke(Wmod, 7633.209517, 10);\r\n    poke(Wmod, 8362.761828, 11);\r\n    poke(Wmod, 8884.677319, 12);\r\n    poke(Wmod, 9562.667766, 13);\r\n    poke(Wmod, 10044.215276, 14);\r\n    poke(Wmod, 10911.039688, 15);\r\n    poke(Wmod, 11230.857653, 16);\r\n    poke(Wmod, 11441.417113, 17);\r\n    poke(Wmod, 12132.573726, 18);\r\n    poke(Wmod, 12329.132521, 19);\r\n    poke(Wmod, 12779.992896, 20);\r\n    poke(Wmod, 13487.223907, 21);\r\n    poke(Wmod, 13812.89152, 22);\r\n    poke(Wmod, 14128.224227, 23);\r\n    poke(Wmod, 14734.279208, 24);\r\n    poke(Wmod, 15686.360266, 25);\r\n    poke(Wmod, 15880.162351, 26);\r\n    poke(Wmod, 16519.575117, 27);\r\n    poke(Wmod, 17246.926539, 28);\r\n    poke(Wmod, 17556.028167, 29);\r\n    poke(Wmod, 18211.477956, 30);\r\n    poke(Wmod, 18420.358618, 31);\r\n    poke(Wmod, 19067.828992, 32);\r\n    poke(Wmod, 19407.986363, 33);\r\n    poke(Wmod, 19969.942067, 34);\r\n    \r\n    poke(Zmod, 0.02806, 0);\r\n    poke(Zmod, 0.030843, 1);\r\n    poke(Zmod, 0.025089, 2);\r\n    poke(Zmod, 0.016473, 3);\r\n    poke(Zmod, 0.028986, 4);\r\n    poke(Zmod, 0.053522, 5);\r\n    poke(Zmod, 0.022354, 6);\r\n    poke(Zmod, 0.017469, 7);\r\n    poke(Zmod, 0.025486, 8);\r\n    poke(Zmod, 0.006351, 9);\r\n    poke(Zmod, 0.016635, 10);\r\n    poke(Zmod, 0.013245, 11);\r\n    poke(Zmod,  0.014157, 12);\r\n    poke(Zmod, 0.003408, 13);\r\n    poke(Zmod, 0.009902, 14);\r\n    poke(Zmod, 0.017948, 15);\r\n    poke(Zmod, 0.026973, 16);\r\n    poke(Zmod, 0.00743, 17);\r\n    poke(Zmod, 0.032272, 18);\r\n    poke(Zmod, 0.005593, 19);\r\n    poke(Zmod, 0.007634, 20);\r\n    poke(Zmod, 0.007395, 21);\r\n    poke(Zmod, 0.034328, 22);\r\n    poke(Zmod, 0.009036, 23); \r\n    poke(Zmod, 0.013227, 24);\r\n    poke(Zmod, 0.01258, 25);\r\n    poke(Zmod, 0.011989, 26);\r\n    poke(Zmod, 0.011913, 27);\r\n    poke(Zmod, 0.005868, 28);\r\n    poke(Zmod, 0.007603, 29);\r\n    poke(Zmod, 0.006733, 30);\r\n    poke(Zmod, 0.014741, 31);\r\n    poke(Zmod, 0.008533, 32);\r\n    poke(Zmod, 0.009627, 33);\r\n    poke(Zmod, 0.007925, 34);\r\n    \n    for (i = 0; i < 88; i += 1) {\r\n\n        Wi = peek(Wmod, i);      // Lire l'élément de Wmod\r\n        Mi = peek(Mmod, i);\r\n        Zi = peek(Zmod, i);\n        \r\n        b = 2 * dt / Mi ;\r\n        a0 = pow(Wi*dt,2) + 4*Zi*Wi*dt + 4;\r\n        a1 = 2 * (pow(Wi*dt,2) - 4);\r\n        a2 = pow(Wi*dt,2) - 4*Zi*Wi*dt + 4;\r\n        \n        poke(bm, b, i);       // Stocker dans bm\r\n        poke(a_m0, a0, i);\r\n        poke(a_m1, a1, i);\r\n        poke(a_m2, a2, i);\n    }\r\n    initialized = 1;\r\n}\r\n\r\n\r\nif (init==0){\r\n    for (i=0; i<88; i+=1) {\r\n        poke(fm_prev, 0, i);\r\n        poke(fm_prev2, 0, i);\r\n        poke(wm_prev, 0, i);\r\n        poke(wm_prev2, 0, i);\r\n    }\r\n    init=1;\r\n}\r\n\r\nq_iR = - (qiL_D + Yc_half*f_D);\r\n\r\nfor (i=0; i<88; i+=1) {\r\n    b = peek(bm, i);\r\n    a1 = peek(a_m1, i);\r\n    a2 = peek(a_m2, i);\r\n    f_prev = peek(fm_prev, i);\r\n    f_prev2 = peek(fm_prev2, i);\r\n    g = b * (-qo_D - qiL_prev2 + qo_D2) - a1*f_prev - a2*f_prev2;\r\n    poke(gm, g, i);\r\n}\r\n\r\ng_over_a0 = 0;\r\nb_over_a0 = 0;\r\nfor (i=0; i<88; i+=1) {\r\n    g = peek(gm, i);\r\n    b = peek(bm, i);\r\n    a0 = peek(a_m0, i);\r\n    g_over_a0 = g_over_a0 + g/a0;\r\n    b_over_a0 = b_over_a0 + b/a0;\r\n}\r\n\r\nq_iL = (-qo_D - Zc*g_over_a0) / (1 + Zc*b_over_a0);\r\nq_h = q_iL + q_iR;\r\nqtot = q_iL - qo_D;\r\nfor (i=0; i<88; i+=1) {\r\n    a1 = peek(a_m1, i);\r\n    a2 = peek(a_m2, i);\r\n    b = peek(bm, i);\r\n    f_prev = peek(fm_prev, i);\r\n    f_prev2 = peek(fm_prev2, i);\r\n    a0 = peek(a_m0, i);\r\n    f = (- a1*f_prev - a2*f_prev2 + b*(qtot - qtot_prev2)) / a0;\r\n    poke(fm, f, i);\r\n}\r\n\r\n//update\r\nfor (i=0; i<88; i+=1) {\r\n    f = peek(fm, i);\r\n    f_prev = peek(fm_prev, i);\r\n    poke(fm_prev2, f_prev, i);\r\n    poke(fm_prev, f, i);\r\n}\r\n\r\nw = q_guess;\r\n\r\n// Algorithme Newton-Raphson (cours Bilbao)\r\ntol = 1e-9;\r\nmaxiters = 50;\r\n\r\nfor (i=0; i<maxiters; i+=1) {\r\n   dicho_val = dicho(w, q_h, Yc_half, vb, Fb, v0);\r\n   dicho_slope = prime_dicho(w, q_h, Yc_half, vb, Fb, v0);\r\n   \r\n   // Débloquer l'algorithme si la pente est trop faible\r\n    if (abs(dicho_slope) < 1e-9) {\r\n       dicho_slope = 1e-9*sign(dicho_slope);\r\n   }\r\n   \r\n   delta = dicho_val / dicho_slope;\r\n   //delta = clamp(delta, -v0, v0); // éviter explosion\r\n   w = w - delta;\r\n   \r\n   if (abs(delta) < tol) {\n        break;\n   }\r\n   \r\n}\r\n\r\nq_guess = w;\r\n\r\nF_val = F_continu(w, vb, Fb, v0); // force au point de contact corde-archet\r\n\r\n// calculs pour le son à écouter\r\nq_oL = q_iR + Yc_half*F_val;\r\nf_b = 1/Yc_half * (qo_halfD - qiL_halfD);\r\nfor (i=0; i<88; i+=1) {\r\n    a0 = peek(a_m0, i);\r\n    a1 = peek(a_m1, i);\r\n    a2 = peek(a_m2, i);\r\n    b = peek(bm, i);\r\n    w_prev = peek(wm_prev, i);\r\n    w_prev2 = peek(wm_prev2, i);\r\n    wi = (- a1*w_prev - a2*w_prev2 + b*(f_b - fb_prev2)) / a0;\r\n    poke(wm, wi, i);\r\n}\r\nv_b = 0;\r\nfor (i=0; i<88; i+=1) {\r\n    wi = peek(wm, i);\r\n    v_b = v_b + wi ;\r\n}\r\n\r\n//update\r\nfor (i=0; i<88; i+=1) {\r\n    wj = peek(wm, i);\r\n    wj_prev = peek(wm_prev, i);\r\n    poke(wm_prev2, wj_prev, i);\r\n    poke(wm_prev, wj, i);\r\n}\r\nfb_prev2 = fb_prev1;\r\nfb_prev1 = f_b;\r\n\r\nout1 = w;\r\nout2 = q_iL;\r\nout3 = q_iR;\r\nout4 = qtot;\r\nout5 = F_val;\r\nout6 = f_b;\r\nout7 = v_b;\r\nout8 = b_over_a0;\r\n",
                                    "fontface": 0,
                                    "fontname": "<Monospaced>",
                                    "fontsize": 12.0,
                                    "id": "obj-33",
                                    "maxclass": "codebox",
                                    "numinlets": 10,
                                    "numoutlets": 8,
                                    "outlettype": [ "", "", "", "", "", "", "", "" ],
                                    "patching_rect": [ 925.9259104728699, 722.2222101688385, 810.0000772476196, 382.307728767395 ]
                                }
                            }
                        ],
                        "lines": [
                            {
                                "patchline": {
                                    "destination": [ "obj-33", 5 ],
                                    "source": [ "obj-10", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-8", 0 ],
                                    "source": [ "obj-12", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-33", 0 ],
                                    "source": [ "obj-28", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-28", 0 ],
                                    "source": [ "obj-29", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-33", 2 ],
                                    "source": [ "obj-3", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-11", 0 ],
                                    "source": [ "obj-33", 5 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-14", 0 ],
                                    "source": [ "obj-33", 7 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-15", 0 ],
                                    "source": [ "obj-33", 6 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-78", 0 ],
                                    "source": [ "obj-33", 1 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-83", 0 ],
                                    "source": [ "obj-33", 2 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-84", 0 ],
                                    "source": [ "obj-33", 4 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-94", 0 ],
                                    "source": [ "obj-33", 3 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-53", 0 ],
                                    "source": [ "obj-40", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-75", 0 ],
                                    "source": [ "obj-40", 2 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-76", 0 ],
                                    "source": [ "obj-40", 3 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-77", 0 ],
                                    "source": [ "obj-40", 1 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-33", 8 ],
                                    "source": [ "obj-68", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-3", 0 ],
                                    "order": 0,
                                    "source": [ "obj-78", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-79", 0 ],
                                    "order": 2,
                                    "source": [ "obj-78", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-81", 0 ],
                                    "order": 1,
                                    "source": [ "obj-78", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-28", 1 ],
                                    "source": [ "obj-79", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-3", 1 ],
                                    "source": [ "obj-8", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-33", 1 ],
                                    "source": [ "obj-81", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-81", 1 ],
                                    "source": [ "obj-82", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-87", 0 ],
                                    "source": [ "obj-83", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-85", 0 ],
                                    "order": 1,
                                    "source": [ "obj-84", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-96", 0 ],
                                    "order": 0,
                                    "source": [ "obj-84", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-87", 1 ],
                                    "source": [ "obj-85", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-85", 1 ],
                                    "source": [ "obj-86", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-10", 0 ],
                                    "order": 0,
                                    "source": [ "obj-87", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-90", 0 ],
                                    "order": 1,
                                    "source": [ "obj-87", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-10", 1 ],
                                    "source": [ "obj-9", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-33", 3 ],
                                    "order": 1,
                                    "source": [ "obj-90", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-92", 0 ],
                                    "order": 0,
                                    "source": [ "obj-90", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-9", 0 ],
                                    "order": 0,
                                    "source": [ "obj-91", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-90", 1 ],
                                    "order": 1,
                                    "source": [ "obj-91", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-33", 4 ],
                                    "source": [ "obj-92", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-95", 0 ],
                                    "source": [ "obj-94", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-33", 6 ],
                                    "source": [ "obj-95", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-33", 7 ],
                                    "source": [ "obj-96", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-96", 1 ],
                                    "source": [ "obj-97", 0 ]
                                }
                            },
                            {
                                "patchline": {
                                    "destination": [ "obj-33", 9 ],
                                    "source": [ "obj-98", 0 ]
                                }
                            }
                        ]
                    },
                    "patching_rect": [ 154.34782314300537, 649.9999876022339, 36.0, 22.0 ],
                    "text": "gen~",
                    "varname": "gen~_AB"
                }
            },
            {
                "box": {
                    "attr": "Fb",
                    "id": "obj-26",
                    "maxclass": "attrui",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 31.14754009246826, 285.24589347839355, 206.55737113952637, 22.0 ]
                }
            },
            {
                "box": {
                    "attr": "L",
                    "id": "obj-28",
                    "maxclass": "attrui",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 263.9344186782837, 272.131139755249, 150.0, 22.0 ]
                }
            },
            {
                "box": {
                    "attr": "mu",
                    "id": "obj-29",
                    "maxclass": "attrui",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 298.5185087323189, 326.6666559576988, 164.0625, 22.0 ]
                }
            },
            {
                "box": {
                    "attr": "x",
                    "id": "obj-33",
                    "maxclass": "attrui",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 278.51850938796997, 299.25924944877625, 171.31147480010986, 22.0 ]
                }
            },
            {
                "box": {
                    "attr": "vb",
                    "id": "obj-34",
                    "maxclass": "attrui",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 10.769231796264648, 260.65573024749756, 150.0, 22.0 ]
                }
            },
            {
                "box": {
                    "attr": "tension",
                    "id": "obj-35",
                    "maxclass": "attrui",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 319.25924879312515, 351.8518403172493, 150.0, 22.0 ]
                }
            },
            {
                "box": {
                    "attr": "v0",
                    "id": "obj-1",
                    "maxclass": "attrui",
                    "numinlets": 1,
                    "numoutlets": 1,
                    "outlettype": [ "" ],
                    "parameter_enable": 0,
                    "patching_rect": [ 53.4482786655426, 309.24589347839355, 150.0, 22.0 ]
                }
            }
        ],
        "lines": [
            {
                "patchline": {
                    "destination": [ "obj-76", 0 ],
                    "source": [ "obj-1", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-53", 0 ],
                    "source": [ "obj-12", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-50", 0 ],
                    "source": [ "obj-13", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-91", 1 ],
                    "source": [ "obj-14", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-91", 0 ],
                    "source": [ "obj-14", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-5", 0 ],
                    "source": [ "obj-15", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-76", 0 ],
                    "source": [ "obj-16", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-10", 0 ],
                    "source": [ "obj-25", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-76", 0 ],
                    "source": [ "obj-26", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-76", 0 ],
                    "source": [ "obj-28", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-76", 0 ],
                    "source": [ "obj-29", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-76", 0 ],
                    "source": [ "obj-33", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-76", 0 ],
                    "source": [ "obj-34", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-76", 0 ],
                    "source": [ "obj-35", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-82", 0 ],
                    "midpoints": [ 1699.4999597072601, 401.4538101875153, 1676.53784770726, 401.4538101875153, 1676.53784770726, 310.0453471875153, 1699.4999597072601, 310.0453471875153 ],
                    "source": [ "obj-45", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-82", 0 ],
                    "source": [ "obj-46", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-76", 0 ],
                    "source": [ "obj-5", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-51", 0 ],
                    "source": [ "obj-50", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-10", 2 ],
                    "source": [ "obj-51", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-10", 1 ],
                    "source": [ "obj-52", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-52", 0 ],
                    "source": [ "obj-53", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-12", 0 ],
                    "order": 3,
                    "source": [ "obj-76", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-14", 0 ],
                    "order": 4,
                    "source": [ "obj-76", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-18", 0 ],
                    "source": [ "obj-76", 2 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-2", 0 ],
                    "order": 0,
                    "source": [ "obj-76", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-3", 0 ],
                    "order": 2,
                    "source": [ "obj-76", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-39", 0 ],
                    "order": 1,
                    "source": [ "obj-76", 0 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-4", 0 ],
                    "source": [ "obj-76", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-37", 0 ],
                    "source": [ "obj-82", 1 ]
                }
            },
            {
                "patchline": {
                    "destination": [ "obj-45", 0 ],
                    "source": [ "obj-82", 0 ]
                }
            }
        ],
        "parameters": {
            "obj-14": [ "live.gain~", "live.gain~", 0 ],
            "parameterbanks": {
                "0": {
                    "index": 0,
                    "name": "",
                    "parameters": [ "-", "-", "-", "-", "-", "-", "-", "-" ],
                    "buttons": [ "-", "-", "-", "-", "-", "-", "-", "-" ]
                }
            },
            "inherited_shortname": 1
        },
        "autosave": 0,
        "styles": [
            {
                "name": "rnbodefault",
                "default": {
                    "accentcolor": [ 0.343034118413925, 0.506230533123016, 0.86220508813858, 1.0 ],
                    "bgcolor": [ 0.031372549019608, 0.125490196078431, 0.211764705882353, 1.0 ],
                    "bgfillcolor": {
                        "angle": 270.0,
                        "autogradient": 0.0,
                        "color": [ 0.031372549019608, 0.125490196078431, 0.211764705882353, 1.0 ],
                        "color1": [ 0.031372549019608, 0.125490196078431, 0.211764705882353, 1.0 ],
                        "color2": [ 0.263682, 0.004541, 0.038797, 1.0 ],
                        "proportion": 0.39,
                        "type": "color"
                    },
                    "color": [ 0.929412, 0.929412, 0.352941, 1.0 ],
                    "elementcolor": [ 0.357540726661682, 0.515565991401672, 0.861786782741547, 1.0 ],
                    "fontname": [ "Lato" ],
                    "fontsize": [ 12.0 ],
                    "stripecolor": [ 0.258338063955307, 0.352425158023834, 0.511919498443604, 1.0 ],
                    "textcolor_inverse": [ 0.968627, 0.968627, 0.968627, 1 ]
                },
                "parentstyle": "",
                "multi": 0
            }
        ]
    }
}