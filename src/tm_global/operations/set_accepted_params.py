from src.tm_global.singleton.current_db_row import CurrentDBRow


def set_accepted_params():
    accepted_states_list = ['MELAKA', 'KELANTAN', 'KEDAH', 'JOHOR', 'NEGERI SEMBILAN', 'PAHANG', 'PERAK', 'PERLIS',
                            'PULAU PINANG', 'SABAH', 'SARAWAK', 'SELANGOR', 'TERENGGANU', 'WILAYAH PERSEKUTUAN',
                            'WILAYAH PERSEKUTUAN LABUAN', 'WILAYAH PERSEKUTUAN PUTRAJAYA']

    accepted_street_types_list = ['ALUR', 'OFF JALAN', 'AVENUE', 'BATU', 'BULATAN', 'CABANG', 'CERUMAN',
                                  'CERUNAN', 'CHANGKAT', 'CROSS', 'DALAMAN', 'DATARAN', 'DRIVE', 'GAT', 'GELUGOR', 'GERBANG',
                                  'GROVE', 'HALA', 'HALAMAN', 'HALUAN', 'HILIR', 'HUJUNG', 'JALAN', 'JAMBATAN', 'JETTY',
                                  'KAMPUNG', 'KELOK', 'LALUAN', 'LAMAN', 'LANE', 'LANGGAK', 'LEBOH', 'LEBUH', 'LEBUHRAYA',
                                  'LEMBAH', 'LENGKOK', 'LENGKONGAN', 'LIKU', 'LILITAN', 'LINGKARAN', 'LINGKONGAN',
                                  'LINGKUNGAN', 'LINTANG', 'LINTASAN', 'LORONG', 'LOSONG', 'LURAH', 'M G', 'MAIN STREET',
                                  'MEDAN', 'PARIT', 'PEKELILING', 'PERMATANG', 'PERSIARAN', 'PERSINT', 'PERSISIRAN', 'PESARA',
                                  'PESIARAN', 'PIASAU', 'PINGGIAN', 'PINGGIR', 'PINGGIRAN', 'PINTAS', 'PINTASAN', 'PUNCAK',
                                  'REGAT', 'ROAD', 'SEBERANG', 'SELASAR', 'SELEKOH', 'SILANG', 'SIMPANG', 'SIMPANGAN',
                                  'SISIRAN', 'SLOPE', 'SOLOK', 'STREET', 'SUSUR', 'SUSURAN', 'TAMAN', 'TANJUNG', 'TEPIAN',
                                  'TINGGIAN', 'TINGKAT', 'P.O.Box', 'PO Box']

    set_accepted_states(accepted_states_list=accepted_states_list)
    set_accepted_street_types(
        accepted_street_types_list=accepted_street_types_list)


def set_accepted_states(accepted_states_list):
    current_db_row = CurrentDBRow.get_instance()
    current_db_row.set_accepted_states_list(
        self=current_db_row, accepted_states_list=accepted_states_list)


def set_accepted_street_types(accepted_street_types_list):
    current_db_row = CurrentDBRow.get_instance()
    current_db_row.set_accepted_street_types_list(
        self=current_db_row, accepted_street_types_list=accepted_street_types_list)
