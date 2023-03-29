from src.tm_partners.operations.login import Login
from src.tm_partners.operations.login import Login
from src.tm_partners.singleton.data_id_range import DataIdRange
from src.tm_partners.coverage_check.coverage_check import FindingCoverage
from src.tm_partners.singleton.image_names import ImageName
from src.tm_partners.operations.set_accepted_params import set_accepted_params
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from src.tm_partners.operations.pause_until_loaded import pause_until_loaded
from src.tm_partners.coverage_check.input_speed_requested import input_speed_requested
from src.tm_partners.operations.select_state import select_state
from src.tm_partners.operations.enter_into_keyword_field import enter_into_keyword_field
from src.tm_partners.operations.click_search_btn import click_search_btn
from src.tm_partners.operations.detect_and_solve_captcha import detect_and_solve_captcha
from src.tm_partners.operations.wait_for_results_table import wait_for_results_table

search_list = [
    ['JOHOR', 'BATU PAHAT', '83400'], ['JOHOR', 'MASAI', '81750'], ['JOHOR', 'JOHOR BAHRU', '079100'], ['JOHOR', 'BATU PAHAT', '83200'], ['JOHOR', 'GELANG PATAH', '81150'], ['JOHOR', 'BANDAR ENDAU', '86900'], ['JOHOR', 'SIMPANG RENGGAM', '86200'], ['JOHOR', 'GELANG PATAH', '81550'], ['JOHOR', 'JOHOR BAHRU', '81100'], ['JOHOR', 'TANGKAK', '84900'], ['JOHOR', 'PALOH', '86600'], ['JOHOR', 'NUSAJAYA', '079250'], ['JOHOR', 'BENUT', '82210'], ['JOHOR', 'JOHOR BAHRU', '80100'], ['JOHOR', 'BANDAR TENGGARA', '81440'], ['JOHOR', 'KULIM', '09000'], ['JOHOR', 'SENAI', '81400'], ['JOHOR', 'LAYANG-LAYANG', '81850'], ['JOHOR', 'KULAI', '84000'], ['JOHOR', 'YONG PENG', '83700'], ['JOHOR', 'PENGERANG', '81600'], ['JOHOR', 'SEGAMAT', '85010'], ['JOHOR', 'KULAI', '81030'], ['JOHOR', 'KOTA TINGGI', '81900'], ['JOHOR', 'GELANG PATAH', '81560'], ['JOHOR', 'DONGGONGON', '89300'], ['JOHOR', 'JOHOR BAHRU', '79100'], ['JOHOR', 'PONTIAN', '82300'], ['JOHOR', 'BATU PAHAT', '83000'], ['JOHOR', 'PONTIAN', '82000'], ['JOHOR', 'PEKAN NANAS', '81500'], ['JOHOR', 'JOHOR BAHRU', '81200'], ['JOHOR', 'JOHOR BAHRU', '80350'], ['JOHOR', 'JOHOR BAHRU', '80300'], ['JOHOR', 'JOHOR BAHRU', '80000'], ['JOHOR', 'PARIT RAJA', '86400'], ['JOHOR', 'JOHOR BAHRU', '80150'], ['JOHOR', 'KANGKAR PULAI JOHOR', '81110'], ['JOHOR', 'SEGAMAT', '85000'], ['JOHOR', 'JEMENTAH', '85200'], ['JOHOR', 'ULU TIRAM', '81800'], ['JOHOR', 'JOHOR BAHRU', '80250'], ['JOHOR', 'KULAI', '81000'], ['JOHOR', 'KOTA TINGGI', '81910'], ['JOHOR', 'YONG PENG', '83710'], ['JOHOR', 'NUSAJAYA', '79250'], ['JOHOR', 'SKUDAI', '83100'], ['JOHOR', 'SEGAMAT', '85020'], ['JOHOR', 'PONTIAN', '82200'], ['JOHOR', 'PASIR GUDANG', '81700'], ['JOHOR', 'MERSING', '86800'], ['JOHOR', 'SEGAMAT', '85100'], ['JOHOR', 'KLUANG', '86000'], ['JOHOR', 'BANDAR PENAWAR', '81930'], ['JOHOR', 'KULAI', '81450'], ['JOHOR', 'TANGKAK', '84400'], ['JOHOR', 'LABIS', '85300'], ['JOHOR', 'SKUDAI', '81300'], ['JOHOR', 'SUNGAI MATI', '84410'], ['KEDAH', 'SUNGAI PETANI', '08600'], ['KEDAH', 'CHANGLOON', '06010'], ['KEDAH', 'ALOR SETAR', '05350'], ['KEDAH', 'KULIM', '09090'], ['KEDAH', 'SIK', '8210'], ['KEDAH', 'KUALA NERANG', '6300'], ['KEDAH', 'ALOR SETAR', '05250'], ['KEDAH', 'KARANGAN', '09400'], ['KEDAH', 'TOKAI, PENDANG', '06660'], ['KEDAH', 'ALOR SETAR', '5050'], ['KEDAH', 'BALING', '09100'], ['KEDAH', 'KARANGAN', '91400'], ['KEDAH', 'BEDONG', '8100'], ['KEDAH', 'SUNGAI PETANI', '8000'], ['KEDAH', 'GURUN', '8300'], ['KEDAH', 'PENDANG', '32300'], ['KEDAH', 'SUNGAI PETANI', '08000'], ['KEDAH', 'KUALA KETIL', '09300'], ['KEDAH', 'JITRA', '06000'], ['KEDAH', 'PENDANG', '06700'], ['KELANTAN', 'JELI', '17610'], ['KELANTAN', 'TUMPAT', '16200'], ['KELANTAN', 'KETEREH', '16450'], ['KELANTAN', 'GUA MUSANG', '18300'], ['KELANTAN', 'MACHANG', '18500'], ['KELANTAN', '', '17500'], ['KELANTAN', 'KOTA BHARU', '16100'], ['KELANTAN', 'PASIR PUTEH', '16800'], ['KELANTAN', 'BACHOK', '16300'], ['KELANTAN', 'SELISING', '16810'], ['KELANTAN', 'KOTA BHARU', '16150'], ['MELAKA', 'KANDANG', '75460'], ['MELAKA', 'BACHANG', '75350'], ['MELAKA', 'MELAKA', '75300'], ['MELAKA', 'MASJID TANAH', '74300'], ['MELAKA', 'MASJID TANAH', '78300'], ['MELAKA', 'BERTAM', '76450'], ['MELAKA', 'ALOR GAJAH', '78000'], ['MELAKA', 'AYER KEROH', '75450'], ['MELAKA', 'BUKIT RAMBAI', '75260'], ['MELAKA', 'DURIAN TUNGGAL', '76100'], ['MELAKA', 'MELAKA', '75200'], ['MELAKA', 'MALIM', '75250'], ['MELAKA', 'MERLIMAU', '77300'], ['PAHANG', 'BERA', '28200'], ['PAHANG', 'KUANTAN', '26070'], ['PAHANG', 'TEMERLOH', '28050'], ['PAHANG', 'BANDAR PUSAT JENGKA', '26400'], ['PAHANG', 'BENTONG', '28700'], ['PAHANG', 'TANAH RATA', '39000'], ['PAHANG', 'TEMERLOH', '28000'], ['PAHANG', 'CHENOR', '28100'], ['PAHANG', 'RAUB', '27500'], ['PAHANG', 'BENTONG', '28740'], ['PAHANG', 'PEKAN', '26600'], ['PAHANG', 'KUALA ROMPIN', '26800'], ['PAHANG', 'RAUB', '27600'], ['PAHANG', 'KARAK', '28600'], ['PAHANG', 'KUALA LIPIS', '27200'], ['PAHANG', 'MUADZAM SHAH', '26700'], ['PAHANG', 'KUANTAN', '25150'], ['PAHANG', 'MENTAKAB', '28400'], ['PAHANG', 'KARAK', '28610'], ['PAHANG', 'KEMAYAN', '28300'], ['PAHANG', 'GENTING HIGHLANDS', '69000'], ['PAHANG', 'KUANTAN', '26100'], ['PAHANG', 'GELUGOR', '11800'], ['PAHANG', 'BRINCHANG', '39100'], ['PAHANG', 'KUANTAN', '26300'], ['PAHANG', 'GELUGOR', '11700'], ['PAHANG', 'DAMAK', '27030'], ['PAHANG', 'KEMAYAN', '28380'], ['PAHANG', 'TANAH RATA', '39010'], ['PAHANG', 'KUANTAN', '26060'], ['PAHANG', 'LANCHANG', '28500'], ['PAHANG', 'JERANTUT', '27000'], ['PERAK', 'TANJUNG MALIM', '35500'], ['PERAK', 'SG.SIPUT(U)', '31100'], ['PERAK', 'PUSING', '31550'], ['PERAK', 'CHEMOR', '31200'], ['PERAK', 'TANJUNG TUALANG', '31800'], ['PERAK', 'ULU KINTA', '31150'], ['PERAK', 'BAGAN SERAI', '34300'], ['PERAK', 'PARIT', '32800'], ['PERAK', 'IPOH', '31650'], ['PERAK', 'PARIT BUNTAR', '34200'], ['PERAK', 'SERI ISKANDAR', '32600'], ['PERAK', 'KUALA SEPETANG', '34650'], ['PERAK', 'GERIK', '33300'], ['PERAK', 'GOPENG', '31600'], ['PERAK', 'SERI MANJUNG', '32040'], ['PERAK', 'SLIM RIVER', '35800'], ['PERAK', 'SELEKOH', '36200'], ['PERAK', 'MALIM NAWAR', '31700'], ['PERAK', 'SEMANGGOL', '34400'], ['PERAK', 'TANJUNG MALIM', '35900'], ['PERAK', 'MANONG', '33800'], ['PERAK', 'IPOH', '30450'], ['PERAK', 'IPOH', '31350'], ['PERAK', 'IPOH', '30010'], ['PERAK', 'IPOH', '30200'], ['PERAK', 'KAMPUNG GAJAH', '36800'], ['PERAK', 'TRONOH', '31750'], ['PERAK', 'HUTAN MELINTANG', '36400'], ['PERAK', 'KUALA KANGSAR', '33000'], ['PERAK', 'TELUK INTAN', '36000'], ['PERAK', 'IPOH', '31250'], ['PERAK', 'KAMPAR', '31900'], ['PERAK', 'SITIAWAN', '32000'], ['PERAK', 'SUNGAI SUMUN', '36300'], ['PERAK', 'IPOH', '31400'], ['PERAK', 'IPOH', '30020'], ['PERAK', 'KERIAN', '34350'], ['PERAK', 'LANGKAP', '36700'], ['PERAK', 'SIMPANG', '34700'], ['PERAK', 'SERI ISKANDAR', '32610'], ['PERAK', 'BAGAN SERAI', '34000'], ['PERAK', 'PANTAI REMIS', '34900'], ['PERAK', 'TAPAH', '35000'], ['PERAK', 'TANJONG PIANDANG', '34250'], ['PERAK', 'AYER TAWAR', '32400'], ['PERAK', 'BATU GAJAH', '31000'], ['PERAK', 'KAMPAR', '31910'], ['PERLIS', 'ARAU', '2600'], ['PERLIS', 'ARAU', '02600'], ['SABAH', 'KOTA KINABALU', '88450'], ['SABAH', 'SIPITANG', '89750'], ['SABAH', 'SANDAKAN', '90000'], ['SABAH', 'TUARAN', '89200'], ['SABAH', 'PUTATAN', '88200'], ['SABAH', 'LAHAD DATU', '91100'], ['SABAH', 'TAWAU', '91000'], ['SABAH', 'BELURAN', '90107'], ['SABAH', 'LABUAN', '87000'], ['SABAH', 'KOTA KINABALU', '89600'], ['SABAH', 'TENOM', '89900'], ['SABAH', 'KOTA KINABALU', '88400'], ['SABAH', 'BONGAWAN', '89700'], ['SABAH', 'TAWAU', '91009'], ['SABAH', 'KOTA KINABATANGAN', '90200'], ['SABAH', 'KOTA KINABALU', '88300'], ['SABAH', 'TONGOD', '89320'], ['SARAWAK', 'LIMBANG', '98700'], ['SARAWAK', 'KUCHING', '93350'], ['SARAWAK', 'KUCHING', '93450'], ['SARAWAK', 'LIMBANG', '98750'], ['SARAWAK', 'KUCHING', '93250'], ['SARAWAK', 'MUKAH', '96400'], ['SARAWAK', 'SEBUYAU', '94850'], ['SARAWAK', 'KUCHING', '93050'], ['SARAWAK', 'SIBU', '96000'], ['SARAWAK', 'BAU', '94000'], ['SARAWAK', 'KOTA SAMARAHAN', '94300'], ['SARAWAK', 'ASAJAYA', '94600'], ['SELANGOR', 'CYBERJAYA', '630000'], ['SELANGOR', 'PETALING JAYA', '47301'], ['SELANGOR', 'GEORGETOWN', '10450'], ['SELANGOR', 'SHAH ALAM', '40300'], ['SELANGOR', 'KAJANG', '43000'], ['SELANGOR', 'TELOK PANGLIMA GARANG', '42500'], ['SELANGOR', 'KLANG', '41000'], ['SELANGOR', 'PUCHONG', '47130'], ['SELANGOR', 'SELANGOR', '46050'], ['SELANGOR', 'PUCHONG', '47100'], ['SELANGOR', 'KAPAR', '41050'], ['SELANGOR', 'KLANG', '41100'], ['SELANGOR', 'BERANANG', '43700'], ['SELANGOR', 'KLANG', '42200'], ['SELANGOR', 'PUCHONG', '471300'], ['SELANGOR', 'SERI KEMBANGAN', '43300'], ['SELANGOR', 'SHAH ALAM', '40000'], ['SELANGOR', 'SERENDAH', '48200'], ['SELANGOR', 'PETALING JAYA', '47300'], ['SELANGOR', 'SHAH ALAM', '40200'], ['SELANGOR', 'PUCHONG', '47160'], ['SELANGOR', 'AMPANG', '68000'], ['SELANGOR', 'SEPANG', '43950'], ['SELANGOR', 'BANDAR BUKIT RAJA', '40150'], ['SELANGOR', 'SHAH ALAM', '40460'], ['SELANGOR', 'BANTING', '42700'], ['SELANGOR', 'SUBANG JAYA', '47610'], ['SELANGOR', 'RASA', '44200'], ['SELANGOR', 'SHAH ALAM', '40400'], ['SELANGOR', 'SHAH ALAM', '42450'], ['SELANGOR', 'KERLING', '44100'], ['SELANGOR', 'PETALING JAYA', '46000'], ['SELANGOR', 'RAWANG', '48000'], ['SELANGOR', 'CHERAS', '43200'], ['SELANGOR', 'SUBANG JAYA', '475000'], ['SELANGOR', 'RAWANG', '48020'], ['SELANGOR', 'RAWANG', '48300'], ['SELANGOR', 'KUALA LUMPUR', '50400'], ['SELANGOR', 'KLANG', '41200'], ['SELANGOR', 'KAPAR', '45800'], ['SELANGOR', 'KLANG', '41150'], ['SELANGOR', 'PUCHONG', '47120'], ['SELANGOR', 'SUBANG JAYA', '47600'], ['SELANGOR', 'KAJANG', '43508'], ['SELANGOR', 'BANDAR BARU BANGI', '43650'], ['SELANGOR', 'PUTRAJAYA', '62050'], ['SELANGOR', 'SHAH ALAM', '40170'], ['SELANGOR', 'KUANG', '48050'], ['SELANGOR', 'SEMENYIH', '43500'], ['SELANGOR', 'KUALA SELANGOR', '45000'], ['SELANGOR', 'SEPANG', '43900'], ['SELANGOR', 'BANDAR PUNCAK ALAM', '42300'], ['SELANGOR', 'KUALA KUBU BHARU', '44010'], ['SELANGOR', 'KUALA SELANGOR', '45700'], ['SELANGOR', 'CYBERJAYA', '63300'], ['SELANGOR', 'PETALING JAYA', '46100'], ['SELANGOR', 'GOMBAK', '53100'], ['SELANGOR', 'JENJAROM', '42600'], ['SELANGOR', 'BATANG KALI', '44300'], ['SELANGOR', 'SUBANG JAYA', '47500'], ['SELANGOR', 'CYBERJAYA', '63000'], ['SELANGOR', 'PETALING JAYA', '47410'], ['SELANGOR', 'DENGKIL', '43800'], ['SELANGOR', 'KLANG', '41300'], ['SELANGOR', 'BESTARI JAYA', '45600'], ['SELANGOR', 'BATU CAVES', '68100'], ['SELANGOR', 'RAWANG', '48010'], ['SELANGOR', 'HULU LANGAT', '43100'], ['SELANGOR', 'KLANG', '41400'], ['SELANGOR', 'BATU ARANG', '48100'], ['SELANGOR', 'PULAU INDAH', '42920'], ['SELANGOR', 'SHAH ALAM', '40470'], ['SELANGOR', 'PUCHONG', '47110'], ['SELANGOR', 'PETALING JAYA', '47830'], ['SELANGOR', 'KLANG', '42940'], ['SELANGOR', 'PETALING JAYA', '47810'], ['SELANGOR', 'TANJONG KARANG', '45500'], ['SELANGOR', 'SHAH ALAM', '40100'], ['SELANGOR', 'PORT KLANG', '42000'], ['SELANGOR', 'PETALING JAYA', '46200'], ['SELANGOR', 'SUNGAI BULOH', '47000'], ['SELANGOR', 'KLANG', '42100'], ['SELANGOR', 'SENAWANG', '71450'], ['SELANGOR', 'SHAH ALAM', '40160'], ['SELANGOR', 'PUCHONG', '47150'], ['SELANGOR', 'PETALING JAYA', '46150'], ['TERENGGANU', 'KUALA TERENGGANU', '21080'], ['TERENGGANU', 'DUNGUN', '23000'], ['TERENGGANU', 'KIJAL', '24100'], ['TERENGGANU', 'KUALA NERUS', '21060'], ['TERENGGANU', 'KUALA BERANG', '21700'], ['TERENGGANU', 'KUALA TERENGGANU', '21100'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '59200'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '53000'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '54100'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '59100'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '51000'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '57100'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '52200'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '57000'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '55000'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '60000'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '58100'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '53300'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '58200'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '59000'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '52100'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '50480'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '58000'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '52000'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '50460'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '56100'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '50250'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '55100'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '55300'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '56000'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '55200'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '51200'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '53200'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '54200'], ['WILAYAH PERSEKUTUAN', 'KUALA LUMPUR', '50150'], ['PULAU PINANG', 'SIMPANG AMPAT', '14120'], ['PULAU PINANG', 'GEORGE TOWN', '10250'], ['PULAU PINANG', 'GEORGE TOWN', '10050'], ['PULAU PINANG', 'KEPALA BATAS', '13200'], ['PULAU PINANG', 'JELUTONG', '11600'], ['PULAU PINANG', 'PENAGA', '13100'], ['PULAU PINANG', 'AIR ITAM', '11060'], ['PULAU PINANG', 'SEBERANG JAYA', '13700'], ['PULAU PINANG', 'PERMATANG PAUH', '13500'], ['PULAU PINANG', 'SIMPANG AMPAT', '14100'], ['PULAU PINANG', 'PERAI', '13600'], ['PULAU PINANG', 'TIMUR LAUT', '11500'], ['PULAU PINANG', 'BUKIT MERTAJAM', '14000'], ['PULAU PINANG', 'BUTTERWORTH', '13020'], ['PULAU PINANG', 'PENANG', '10350'], ['PULAU PINANG', 'TANJUNG TOKONG', '10470'], ['PULAU PINANG', 'GEORGETOWN', '10150'], ['PULAU PINANG', 'BAYAN LEPAS', '11900'], ['PULAU PINANG', 'BALIK PULAU', '11000'], ['PULAU PINANG', 'BAYAN LEPAS', '11920'], ['PULAU PINANG', 'GEORGETOWN', '10400'], ['PULAU PINANG', 'GEORGETOWN', '11200'], ['NEGERI SEMBILAN', 'KUALA PILAH', '71500'], ['NEGERI SEMBILAN', 'SEREMBAN', '70200'], ['NEGERI SEMBILAN', 'LABU', '71350'], ['NEGERI SEMBILAN', 'GEMAS', '73400'], ['NEGERI SEMBILAN', 'JOHOL', '73100'], ['NEGERI SEMBILAN', 'SEREMBAN', '70300'], ['NEGERI SEMBILAN', 'BANDAR ENSTEK', '71760'], ['NEGERI SEMBILAN', 'KUALA PILAH', '72000'], ['NEGERI SEMBILAN', 'SEREMBAN', '70400'], ['NEGERI SEMBILAN', 'GEMAS', '73430'], ['NEGERI SEMBILAN', 'SEREMBAN', '50200'], ['NEGERI SEMBILAN', 'LABU', '71900'], ['NEGERI SEMBILAN', 'KUALA PILAH', '71550'], ['NEGERI SEMBILAN', 'PUSAT BANDAR SERTING', '72120'], ['NEGERI SEMBILAN', 'PORT DICKSON', '71050'], ['NEGERI SEMBILAN', 'REMBAU', '71300'], ['NEGERI SEMBILAN', 'JEMPOL', '72100'], ['NEGERI SEMBILAN', 'MANTIN', '71700'], ['NEGERI SEMBILAN', 'PEDAS', '71400'], ['NEGERI SEMBILAN', 'LENGGENG', '71750'], ['NEGERI SEMBILAN', 'SEREMBAN', '70450'], ['NEGERI SEMBILAN', 'PORT DICKSON', '71000'], ['NEGERI SEMBILAN', 'KUALA PILAH', '72500'], ['NEGERI SEMBILAN', 'SEREMBAN', '70100'], ['NEGERI SEMBILAN', 'GEMAS', '73470'], ['NEGERI SEMBILAN', 'NILAI', '71800']
    ]

image_name = ImageName.get_instance()
image_name.set_full_page_image_name(
    self=image_name, full_page_image_name="thread_name_full_page.png")
image_name.set_captcha_image_name(
    self=image_name, captcha_image_name="thread_name_captcha.png")

login = Login()
(driver, a) = login.login()
finding_coverage = FindingCoverage()
set_accepted_params()

(driver, a) = input_speed_requested(driver, a, 50)
(driver, a) = pause_until_loaded(driver, a)

max_count = -1
min_count = 5000
current_count = 0
freq = {}
for item in search_list:
    current_count += 1
    
    state = item [0]
    city = item [1] # doesn't help in the search
    postcode = item [2]
    
    (driver, a) = select_state(driver, a, state)
    (driver, a) = enter_into_keyword_field(
        driver, a, postcode)
    (driver, a) = click_search_btn(driver, a)

    (driver, a) = detect_and_solve_captcha(driver, a)

    # wait for the results table to pop up.
    try:
        (driver, a) = pause_until_loaded(driver, a)
        (driver, a) = wait_for_results_table(driver, a)
    except TimeoutException:
        (driver, a) = detect_and_solve_captcha(driver, a)
    # captcha should be solved now. getting the results...
    (driver, a) = pause_until_loaded(driver, a)

    rows = driver.find_elements(
        By.XPATH, "//*[@id='resultAddressGrid']/tbody/tr")
    
    row_count = len(rows)-2 if len(rows)-2 >=1 else 0
    
    address_count = [int(s) for s in driver.find_element(
        By.XPATH, "//*[@id='serviceabilityCheck_checkAddressServiceability_1_12']/div[1]/div/div[10]/div[1]/table[1]/tbody/tr/td").text.split() if s.isdigit()][0]

    if(row_count == address_count):
        if address_count in freq:
            freq[address_count] += 1
        else:
            freq[address_count] = 1

        max_count = max(max_count, address_count)
        min_count = min(min_count, address_count)
    else:
        print("Counts are different ----------------")
        print(current_count, row_count, address_count, state, city, postcode)

    progress_perc = (current_count / len(search_list)) * 100
    if round(progress_perc,0) % 5 == 0:
        print('>>>>>>>>', progress_perc, "% completed")
        print('Current Max:', max_count)
        print('Current Min:', min_count)
    
print('Max:', max_count, 'Freq:', freq[max_count])
print('Min:', min_count, 'Freq:', freq[min_count])

# read_from_db()
# finding_coverage.finding_coverage(
#     driver=driver, a=a)
driver.quit()