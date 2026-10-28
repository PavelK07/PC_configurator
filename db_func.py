def db_connect(db_file_name):
    conn = sqlite3.connect(db_file_name)
    cursor = conn.cursor()
    return cursor, conn

def ensure_tables(cursor):
    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS cpu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            brand TEXT NOT NULL,
            series INTEGER, -- номер серии 3,5,7,9
            cores INTEGER NOT NULL,
            tdp INTEGER NOT NULL,
            performance FLOAT, --производительность с technical.city
            socket TEXT NOT NULL,
            release_year INTEGER,
            mem_type INTEGER NOT NULL,
            max_mem INTEGER,
            integrated_graphics BOOL NOT NULL, --есть или нет
            pci_e_controller_version INTEGER,
            pci_e_lines_count INTEGER
        );

        CREATE TABLE IF NOT EXISTS ram (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            brand TEXT,
            mem_type INTEGER NOT NULL, --3,4 или 5 ддр
            module_count INTEGER NOT NULL, --количество в комплекте
            total_capacity INTEGER NOT NULL, --суммарный объем модулей
            module_capacity INTEGER,
            frequency INTEGER,
            timings TEXT, --пример: 'CL16-18-18-38'
            release_year INTEGER
        );
        
        CREATE TABLE IF NOT EXISTS mother_board (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            brand TEXT,
            series TEXT,
            chitset TEXT,
            form_factor TEXT NOT NULL,
            socket TEXT NOT NULL,
            mem_type INTEGER NOT NULL,
            mem_slots INTEGER NOT NULL,
            max_mem INTEGER,
            pci_e_slots_count INTEGER NOT NULL,
            main_pci_e_slot_version INTEGER, --версия pci
            mvme_slots_count INTEGER NOT NULL,
            mvme_form_factors_support TEXT,
            main_mvme_slot_pci_e_version INTEGER,
            sata_ports_count INTEGER NOT NULL,
            sata_cable_count INTEGER,
            lan_ports_count INTEGER NOT NULL,
            usb_a_ports_count INTEGER,
            usb_3_2_gen2_ports_count INTEGER,
            usb_c_ports_count INTEGER,
            usb_c_version TEXT,
            hdmi_ports_count INTEGER,
            dp_ports_count INTEGER,
            vga_ports_count INTEGER,
            dvi_ports_count INTEGER,
            cpu_fan_power_connector INTEGER, --количество
            case_fan_connectors_count INTEGER, --4pin
            argb_connectors_count INTEGER, --5V-D-G 3pin
            rgb_connectors_count INTEGER, --12V-G-R-B 4pin
            main_power_connector INTEGER, --24pin 
            cpu_power_connector TEXT,  --6/8/8x2
            power_phases INTEGER, --10+2+1 = 10
            color TEXT,
            release_year INTEGER
        );
        
        CREATE TABLE IF NOT EXISTS gpu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            brand TEXT,
            release_year INTEGER,
            color TEXT,
            model TEXT,
            lenght FLOAT, --в миллиметрах
            hight FLOAT, --количество занимаемых слотов по высоте
            low_profile BOOL, --да или нет
            tdp INTEGER, --энергопотребление, можно с technical.city
            performance FLOAT, --производительность с technical.city
            recomendet_power_block_power INTEGER,
            addition_power_conectors_type INTEGER, --8 or 16 pin
            addition_power_conectors_count INTEGER,
            coolers_count INTEGER,
            video_mem_capacity INTEGER NOT NULL,
            mem_bus_width INTEGER,
            max_mem_bandwidth INTEGER,
            pci_e_version INTEGER,
            pci_e_lines_count INTEGER,
            hdmi_ports_count INTEGER,
            dp_ports_count INTEGER,
            vga_ports_count INTEGER,
            dvi_ports_count INTEGER,
            hdmi_version TEXT,
            dp_version TEXT,
            max_displays INTEGER,
            max_resolution TEXT,
            rgb BOOL NOT NULL   --есть или нет
        );

        CREATE TABLE IF NOT EXISTS ssd_sata(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            brand TEXT,
            size_type TEXT,
            capacity INTEGER NOT NULL,
            buffer BOOL,   --есть или нет
            max_speed_write INTEGER,
            max_speed_read INTEGER,
            max_rec_lifeespan INTEGER
        );

        CREATE TABLE IF NOT EXISTS ssd_mvme(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            brand TEXT,
            form_factor TEXT,
            capacity INTEGER NOT NULL,
            buffer BOOL,  --есть или нет
            max_speed_write INTEGER,
            max_speed_read INTEGER,
            max_rec_lifeespan INTEGER,
            pci_e_version INTEGER
        );

        CREATE TABLE IF NOT EXISTS hdd (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            brand TEXT,
            form_factor TEXT,
            capacity INTEGER NOT NULL,
            buffer BOOL,  --есть или нет
            max_data_trans_speed INTEGER
        );  

        CREATE TABLE IF NOT EXISTS power_block (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            brand TEXT,
            power INTEGER NOT NULL,
            form_factor TEXT,
            color TEXT,
            main_power_connector TEXT, --20+4 pin = [20,4]
            cpu_power_connector TEXT,  --2 x 4+4 pin = 2*[4,4]
            gpu_power_connector TEXT,  -- 2 x 6+2 pin = 2*[6,2]
            sata_power_connector_count INTEGER,
            molex_count INTEGER,
            standart_80_plus TEXT,
            protection_tecnologies TEXT
        );      
        
        CREATE TABLE IF NOT EXISTS cpu_cooler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price INTEGER NOT NULL,
            brand TEXT,
            fan_power_connector INTEGER NOT NULL,
            bearing_type TEXT,
            hight FLOAT NOT NULL, --в миллиметрах
            color TEXT,
            heat_pipes INTEGER NOT NULL,
            heat_dissipation INTEGER NOT NULL,
            sockets TEXT NOT NULL,     --строкой список сокетов через запятую
            rgb BOOL NOT NULL,    --есть или нет
            rgb_power_connector INTEGER,
            fan_included INTEGER NOT NULL,
            fan_size INTEGER     --чтобы знарь какой нада, если нет комплектного
        )
    """)
    conn.commit()
