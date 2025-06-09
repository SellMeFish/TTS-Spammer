import random
import json
import requests
import time
from datetime import datetime, timedelta
from colorama import Fore, Style, init

init()

def print_colored(text, color=Fore.WHITE):
    print(f"{color}{text}{Style.RESET_ALL}")

def luhn_checksum(card_num):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_num)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10

def calculate_luhn(partial_card_number):
    check_digit = luhn_checksum(int(partial_card_number) * 10)
    return 0 if check_digit == 0 else 10 - check_digit

def generate_visa():
    visa_prefixes = ["4532", "4556", "4716", "4929", "4485", "4024", "4539", "4556", "4916", "4532", "4485", "4716"]
    prefix = random.choice(visa_prefixes)
    for _ in range(11):
        prefix += str(random.randint(0, 9))
    check_digit = calculate_luhn(prefix)
    return prefix + str(check_digit)

def generate_mastercard():
    mc_prefixes = ["5555", "5105", "5205", "5305", "5405", "5505", "5174", "5254", "5334", "5414", "5494", "5574", "2221", "2720"]
    prefix = random.choice(mc_prefixes)
    for _ in range(11):
        prefix += str(random.randint(0, 9))
    check_digit = calculate_luhn(prefix)
    return prefix + str(check_digit)

def generate_amex():
    amex_prefixes = ["3782", "3714", "3716", "3717", "3728", "3744", "3747", "3748", "3787", "3704", "3705", "3708"]
    prefix = random.choice(amex_prefixes)
    for _ in range(10):
        prefix += str(random.randint(0, 9))
    check_digit = calculate_luhn(prefix)
    return prefix + str(check_digit)

def generate_discover():
    discover_prefixes = ["6011", "6221", "6229", "6247", "6269", "6273", "6277", "6282", "6295", "6297", "6375", "6394", "6404", "6411", "6421", "6490", "6500", "6504", "6505", "6506", "6507", "6508", "6509", "6516", "6550", "6551", "6552", "6553", "6554", "6555"]
    prefix = random.choice(discover_prefixes)
    for _ in range(11):
        prefix += str(random.randint(0, 9))
    check_digit = calculate_luhn(prefix)
    return prefix + str(check_digit)

def generate_jcb():
    prefix = "35" + str(random.randint(28, 89))
    for _ in range(11):
        prefix += str(random.randint(0, 9))
    check_digit = calculate_luhn(prefix)
    return prefix + str(check_digit)

def generate_diners():
    prefix = "30" + str(random.randint(0, 5))
    for _ in range(10):
        prefix += str(random.randint(0, 9))
    check_digit = calculate_luhn(prefix)
    return prefix + str(check_digit)

def generate_expiry_date():
    current_year = datetime.now().year
    future_year = current_year + random.randint(1, 8)
    month = random.randint(1, 12)
    return f"{month:02d}/{str(future_year)[2:]}"

def generate_cvv(card_type):
    if card_type.lower() == "amex":
        return str(random.randint(1000, 9999))
    else:
        return str(random.randint(100, 999))

def get_random_name_from_api():
    try:
        response = requests.get("https://randomuser.me/api/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            user = data['results'][0]
            first = user['name']['first'].title()
            last = user['name']['last'].title()
            return f"{first} {last}"
    except:
        pass
    return None

def generate_cardholder_name():
    api_name = get_random_name_from_api()
    if api_name:
        return api_name
    
    first_names = [
        "Alexander", "Benjamin", "Christopher", "Daniel", "Edward", "Frederick", "Gabriel", "Harrison", "Isaac", "Jonathan",
        "Katherine", "Lillian", "Margaret", "Natalie", "Olivia", "Patricia", "Rebecca", "Samantha", "Victoria", "Williamson",
        "Abigail", "Charlotte", "Elizabeth", "Isabella", "Madison", "Sophia", "Emma", "Ava", "Mia", "Harper",
        "Ethan", "Mason", "Logan", "Lucas", "Jackson", "Aiden", "Oliver", "Elijah", "James", "William",
        "Amelia", "Evelyn", "Abigail", "Emily", "Elizabeth", "Mila", "Ella", "Avery", "Sofia", "Camila",
        "Sebastian", "Mateo", "Ezra", "Elias", "Carter", "Jayden", "Luca", "Anthony", "Dylan", "Lincoln",
        "Grace", "Chloe", "Victoria", "Penelope", "Layla", "Lillian", "Addison", "Natalie", "Ellie", "Maya"
    ]
    
    last_names = [
        "Anderson", "Thompson", "Martinez", "Robinson", "Rodriguez", "Lewis", "Walker", "Hall", "Allen", "Young",
        "Hernandez", "King", "Wright", "Lopez", "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez",
        "Nelson", "Carter", "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans",
        "Edwards", "Collins", "Stewart", "Sanchez", "Morris", "Rogers", "Reed", "Cook", "Morgan", "Bell",
        "Murphy", "Bailey", "Rivera", "Cooper", "Richardson", "Cox", "Howard", "Ward", "Torres", "Peterson",
        "Gray", "Ramirez", "James", "Watson", "Brooks", "Kelly", "Sanders", "Price", "Bennett", "Wood"
    ]
    
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def get_random_address_from_api():
    try:
        response = requests.get("https://randomuser.me/api/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            user = data['results'][0]
            location = user['location']
            
            street_number = location['street']['number']
            street_name = location['street']['name']
            city = location['city'].title()
            state = location['state'].title()
            postcode = str(location['postcode'])
            country = location['country'].upper()
            
            return {
                "street": f"{street_number} {street_name}",
                "city": city,
                "state": state,
                "zip": postcode,
                "country": country
            }
    except:
        pass
    return None

def generate_billing_address():
    api_address = get_random_address_from_api()
    if api_address:
        return api_address
    
    street_numbers = [str(random.randint(100, 9999))]
    street_names = [
        "Sunset Boulevard", "Broadway", "Fifth Avenue", "Wall Street", "Madison Avenue", "Park Avenue",
        "Rodeo Drive", "Hollywood Boulevard", "Michigan Avenue", "State Street", "Commonwealth Avenue",
        "Pennsylvania Avenue", "Constitution Avenue", "Independence Avenue", "Connecticut Avenue",
        "Massachusetts Avenue", "Wisconsin Avenue", "Georgia Avenue", "New Hampshire Avenue",
        "Vermont Avenue", "Rhode Island Avenue", "Delaware Avenue", "Maryland Avenue", "Virginia Avenue",
        "North Carolina Avenue", "South Carolina Avenue", "Tennessee Avenue", "Kentucky Avenue",
        "Louisiana Avenue", "Mississippi Avenue", "Alabama Avenue", "Florida Avenue", "Texas Avenue"
    ]
    
    cities_states = [
        ("New York", "NY"), ("Los Angeles", "CA"), ("Chicago", "IL"), ("Houston", "TX"), ("Phoenix", "AZ"),
        ("Philadelphia", "PA"), ("San Antonio", "TX"), ("San Diego", "CA"), ("Dallas", "TX"), ("San Jose", "CA"),
        ("Austin", "TX"), ("Jacksonville", "FL"), ("Fort Worth", "TX"), ("Columbus", "OH"), ("Charlotte", "NC"),
        ("San Francisco", "CA"), ("Indianapolis", "IN"), ("Seattle", "WA"), ("Denver", "CO"), ("Washington", "DC"),
        ("Boston", "MA"), ("El Paso", "TX"), ("Nashville", "TN"), ("Detroit", "MI"), ("Oklahoma City", "OK"),
        ("Portland", "OR"), ("Las Vegas", "NV"), ("Memphis", "TN"), ("Louisville", "KY"), ("Baltimore", "MD"),
        ("Milwaukee", "WI"), ("Albuquerque", "NM"), ("Tucson", "AZ"), ("Fresno", "CA"), ("Sacramento", "CA"),
        ("Mesa", "AZ"), ("Kansas City", "MO"), ("Atlanta", "GA"), ("Long Beach", "CA"), ("Colorado Springs", "CO"),
        ("Raleigh", "NC"), ("Miami", "FL"), ("Virginia Beach", "VA"), ("Omaha", "NE"), ("Oakland", "CA"),
        ("Minneapolis", "MN"), ("Tulsa", "OK"), ("Arlington", "TX"), ("Tampa", "FL"), ("New Orleans", "LA")
    ]
    
    street = f"{random.choice(street_numbers)} {random.choice(street_names)}"
    city, state = random.choice(cities_states)
    zip_code = str(random.randint(10001, 99999))
    
    return {
        "street": street,
        "city": city,
        "state": state,
        "zip": zip_code,
        "country": "US"
    }

def validate_card_number(card_number):
    try:
        return luhn_checksum(int(card_number)) == 0
    except:
        return False

def get_card_type(card_number):
    if card_number.startswith('4'):
        return "Visa"
    elif card_number.startswith('5') or card_number.startswith('2'):
        return "Mastercard"
    elif card_number.startswith('3'):
        if card_number.startswith('34') or card_number.startswith('37'):
            return "American Express"
        elif card_number.startswith('30') or card_number.startswith('36') or card_number.startswith('38'):
            return "Diners Club"
        elif card_number.startswith('35'):
            return "JCB"
    elif card_number.startswith('6'):
        return "Discover"
    return "Unknown"

def format_card_number(card_number):
    if len(card_number) == 15:
        return f"{card_number[:4]} {card_number[4:10]} {card_number[10:]}"
    elif len(card_number) == 16:
        return f"{card_number[:4]} {card_number[4:8]} {card_number[8:12]} {card_number[12:]}"
    elif len(card_number) == 14:
        return f"{card_number[:4]} {card_number[4:10]} {card_number[10:]}"
    else:
        return card_number

def generate_phone_number():
    area_codes = ["201", "202", "203", "205", "206", "207", "208", "209", "210", "212", "213", "214", "215", "216", "217", "218", "219", "224", "225", "228", "229", "231", "234", "239", "240", "248", "251", "252", "253", "254", "256", "260", "262", "267", "269", "270", "276", "281", "301", "302", "303", "304", "305", "307", "308", "309", "310", "312", "313", "314", "315", "316", "317", "318", "319", "320", "321", "323", "325", "330", "331", "334", "336", "337", "339", "347", "351", "352", "360", "361", "386", "401", "402", "404", "405", "406", "407", "408", "409", "410", "412", "413", "414", "415", "417", "419", "423", "424", "425", "430", "432", "434", "435", "440", "443", "445", "464", "469", "470", "475", "478", "479", "480", "484", "501", "502", "503", "504", "505", "507", "508", "509", "510", "512", "513", "515", "516", "517", "518", "520", "530", "540", "541", "551", "559", "561", "562", "563", "564", "567", "570", "571", "573", "574", "575", "580", "585", "586", "601", "602", "603", "605", "606", "607", "608", "609", "610", "612", "614", "615", "616", "617", "618", "619", "620", "623", "626", "630", "631", "636", "641", "646", "650", "651", "660", "661", "662", "667", "678", "682", "701", "702", "703", "704", "706", "707", "708", "712", "713", "714", "715", "716", "717", "718", "719", "720", "724", "727", "731", "732", "734", "737", "740", "747", "754", "757", "760", "762", "763", "765", "770", "772", "773", "774", "775", "781", "785", "786", "787", "801", "802", "803", "804", "805", "806", "808", "810", "812", "813", "814", "815", "816", "817", "818", "828", "830", "831", "832", "843", "845", "847", "848", "850", "856", "857", "858", "859", "860", "862", "863", "864", "865", "870", "872", "878", "901", "903", "904", "906", "907", "908", "909", "910", "912", "913", "914", "915", "916", "917", "918", "919", "920", "925", "928", "929", "931", "936", "937", "940", "941", "947", "949", "951", "952", "954", "956", "959", "970", "971", "972", "973", "978", "979", "980", "984", "985", "989"]
    area_code = random.choice(area_codes)
    exchange = str(random.randint(200, 999))
    number = str(random.randint(1000, 9999))
    return f"({area_code}) {exchange}-{number}"

def generate_email_address(name):
    domains = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "aol.com", "icloud.com", "protonmail.com", "mail.com"]
    name_parts = name.lower().split()
    
    email_formats = [
        f"{name_parts[0]}.{name_parts[1]}",
        f"{name_parts[0]}{name_parts[1]}",
        f"{name_parts[0][0]}{name_parts[1]}",
        f"{name_parts[0]}.{name_parts[1][0]}",
        f"{name_parts[0]}{random.randint(1, 999)}",
        f"{name_parts[0]}.{name_parts[1]}{random.randint(1, 99)}"
    ]
    
    email_name = random.choice(email_formats)
    domain = random.choice(domains)
    return f"{email_name}@{domain}"

def generate_ssn():
    area = random.randint(100, 999)
    group = random.randint(10, 99)
    serial = random.randint(1000, 9999)
    return f"{area}-{group}-{serial}"

def generate_card_data(card_type):
    generators = {
        "visa": generate_visa,
        "mastercard": generate_mastercard,
        "amex": generate_amex,
        "discover": generate_discover,
        "jcb": generate_jcb,
        "diners": generate_diners
    }
    
    if card_type.lower() not in generators:
        return None
    
    card_number = generators[card_type.lower()]()
    expiry = generate_expiry_date()
    cvv = generate_cvv(card_type)
    name = generate_cardholder_name()
    address = generate_billing_address()
    phone = generate_phone_number()
    email = generate_email_address(name)
    ssn = generate_ssn()
    
    return {
        "card_number": card_number,
        "formatted_number": format_card_number(card_number),
        "card_type": get_card_type(card_number),
        "expiry_date": expiry,
        "cvv": cvv,
        "cardholder_name": name,
        "billing_address": address,
        "phone_number": phone,
        "email_address": email,
        "ssn": ssn,
        "valid": validate_card_number(card_number)
    }

def display_card_info(card_data):
    if not card_data:
        print_colored("[ERROR] No card data to display!", Fore.RED)
        return
    
    print_colored("\n" + "=" * 70, Fore.CYAN)
    print_colored("              GENERATED CREDIT CARD", Fore.WHITE)
    print_colored("=" * 70, Fore.CYAN)
    
    print_colored(f"\n--- CARD INFORMATION ---", Fore.YELLOW)
    print_colored(f"Card Type: {card_data['card_type']}", Fore.YELLOW)
    print_colored(f"Card Number: {card_data['formatted_number']}", Fore.WHITE)
    print_colored(f"Raw Number: {card_data['card_number']}", Fore.CYAN)
    print_colored(f"Expiry Date: {card_data['expiry_date']}", Fore.GREEN)
    print_colored(f"CVV: {card_data['cvv']}", Fore.MAGENTA)
    
    print_colored(f"\n--- CARDHOLDER INFORMATION ---", Fore.YELLOW)
    print_colored(f"Full Name: {card_data['cardholder_name']}", Fore.BLUE)
    print_colored(f"Phone Number: {card_data['phone_number']}", Fore.BLUE)
    print_colored(f"Email Address: {card_data['email_address']}", Fore.BLUE)
    print_colored(f"SSN: {card_data['ssn']}", Fore.BLUE)
    
    print_colored(f"\n--- BILLING ADDRESS ---", Fore.YELLOW)
    address = card_data['billing_address']
    print_colored(f"Street: {address['street']}", Fore.WHITE)
    print_colored(f"City: {address['city']}", Fore.WHITE)
    print_colored(f"State: {address['state']}", Fore.WHITE)
    print_colored(f"ZIP: {address['zip']}", Fore.WHITE)
    print_colored(f"Country: {address['country']}", Fore.WHITE)
    
    validation_color = Fore.GREEN if card_data['valid'] else Fore.RED
    validation_text = "VALID" if card_data['valid'] else "INVALID"
    print_colored(f"\n--- VALIDATION ---", Fore.YELLOW)
    print_colored(f"Luhn Check: {validation_text}", validation_color)

def save_cards_to_file(cards, filename="generated_cards.json"):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(cards, f, indent=2, ensure_ascii=False)
        print_colored(f"[SUCCESS] Cards saved to {filename}", Fore.GREEN)
    except Exception as e:
        print_colored(f"[ERROR] Failed to save cards: {str(e)}", Fore.RED)

def export_cards_csv(cards, filename="generated_cards.csv"):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("Card Type,Card Number,Expiry Date,CVV,Cardholder Name,Phone,Email,SSN,Street,City,State,ZIP,Country,Valid\n")
            for card in cards:
                address = card['billing_address']
                f.write(f"{card['card_type']},{card['card_number']},{card['expiry_date']},{card['cvv']},{card['cardholder_name']},{card['phone_number']},{card['email_address']},{card['ssn']},{address['street']},{address['city']},{address['state']},{address['zip']},{address['country']},{card['valid']}\n")
        print_colored(f"[SUCCESS] Cards exported to {filename}", Fore.GREEN)
    except Exception as e:
        print_colored(f"[ERROR] Failed to export cards: {str(e)}", Fore.RED)

def run_credit_card_generator():
    print_colored("=" * 60, Fore.CYAN)
    print_colored("         CREDIT CARD GENERATOR", Fore.WHITE)
    print_colored("=" * 60, Fore.CYAN)
    print_colored("FOR TESTING PURPOSES ONLY", Fore.RED)
    print_colored("=" * 60, Fore.CYAN)
    
    generated_cards = []
    
    while True:
        print_colored("\nSelect card type:", Fore.WHITE)
        print_colored("1. Visa", Fore.YELLOW)
        print_colored("2. Mastercard", Fore.YELLOW)
        print_colored("3. American Express", Fore.YELLOW)
        print_colored("4. Discover", Fore.YELLOW)
        print_colored("5. JCB", Fore.YELLOW)
        print_colored("6. Diners Club", Fore.YELLOW)
        print_colored("7. Generate Random", Fore.YELLOW)
        print_colored("8. Bulk Generate", Fore.YELLOW)
        print_colored("9. Validate Card Number", Fore.YELLOW)
        print_colored("10. BIN Checker", Fore.YELLOW)
        print_colored("11. Export Generated Cards", Fore.YELLOW)
        print_colored("12. Exit", Fore.RED)
        
        choice = input(f"\n{Fore.WHITE}Enter choice (1-12): {Style.RESET_ALL}").strip()
        
        if choice == '1':
            card_data = generate_card_data("visa")
            if card_data:
                display_card_info(card_data)
                generated_cards.append(card_data)
                
        elif choice == '2':
            card_data = generate_card_data("mastercard")
            if card_data:
                display_card_info(card_data)
                generated_cards.append(card_data)
                
        elif choice == '3':
            card_data = generate_card_data("amex")
            if card_data:
                display_card_info(card_data)
                generated_cards.append(card_data)
                
        elif choice == '4':
            card_data = generate_card_data("discover")
            if card_data:
                display_card_info(card_data)
                generated_cards.append(card_data)
                
        elif choice == '5':
            card_data = generate_card_data("jcb")
            if card_data:
                display_card_info(card_data)
                generated_cards.append(card_data)
                
        elif choice == '6':
            card_data = generate_card_data("diners")
            if card_data:
                display_card_info(card_data)
                generated_cards.append(card_data)
                
        elif choice == '7':
            card_types = ["visa", "mastercard", "amex", "discover", "jcb", "diners"]
            random_type = random.choice(card_types)
            card_data = generate_card_data(random_type)
            if card_data:
                display_card_info(card_data)
                generated_cards.append(card_data)
                
        elif choice == '8':
            try:
                count = int(input(f"{Fore.WHITE}How many cards to generate? {Style.RESET_ALL}"))
                if count <= 0 or count > 1000:
                    print_colored("[ERROR] Please enter a number between 1 and 1000", Fore.RED)
                    continue
                
                print_colored(f"[INFO] Generating {count} cards...", Fore.CYAN)
                card_types = ["visa", "mastercard", "amex", "discover", "jcb", "diners"]
                
                for i in range(count):
                    card_type = random.choice(card_types)
                    card_data = generate_card_data(card_type)
                    if card_data:
                        generated_cards.append(card_data)
                        if i % 10 == 0:
                            print_colored(f"Generated {i+1}/{count} cards...", Fore.YELLOW)
                
                print_colored(f"[SUCCESS] Generated {count} cards successfully!", Fore.GREEN)
                
            except ValueError:
                print_colored("[ERROR] Invalid number!", Fore.RED)
                
        elif choice == '9':
            card_number = input(f"{Fore.WHITE}Enter card number to validate: {Style.RESET_ALL}").strip().replace(' ', '')
            if card_number:
                is_valid = validate_card_number(card_number)
                card_type = get_card_type(card_number)
                formatted = format_card_number(card_number)
                
                print_colored(f"\nCard Number: {formatted}", Fore.WHITE)
                print_colored(f"Card Type: {card_type}", Fore.YELLOW)
                validation_color = Fore.GREEN if is_valid else Fore.RED
                validation_text = "VALID" if is_valid else "INVALID"
                print_colored(f"Validation: {validation_text}", validation_color)
            else:
                print_colored("[ERROR] No card number provided!", Fore.RED)
                
        elif choice == '10':
            bin_number = input(f"{Fore.WHITE}Enter BIN (first 6 digits): {Style.RESET_ALL}").strip()
            if bin_number and len(bin_number) >= 6:
                try:
                    response = requests.get(f"https://lookup.binlist.net/{bin_number[:6]}", timeout=10)
                    if response.status_code == 200:
                        bin_data = response.json()
                        print_colored(f"\n--- BIN INFORMATION ---", Fore.YELLOW)
                        print_colored(f"BIN: {bin_number[:6]}", Fore.WHITE)
                        print_colored(f"Brand: {bin_data.get('brand', 'Unknown').title()}", Fore.CYAN)
                        print_colored(f"Type: {bin_data.get('type', 'Unknown').title()}", Fore.CYAN)
                        print_colored(f"Level: {bin_data.get('level', 'Unknown').title()}", Fore.CYAN)
                        
                        bank = bin_data.get('bank', {})
                        if bank:
                            print_colored(f"Bank: {bank.get('name', 'Unknown')}", Fore.GREEN)
                            print_colored(f"Phone: {bank.get('phone', 'Unknown')}", Fore.GREEN)
                            print_colored(f"URL: {bank.get('url', 'Unknown')}", Fore.GREEN)
                        
                        country = bin_data.get('country', {})
                        if country:
                            print_colored(f"Country: {country.get('name', 'Unknown')}", Fore.BLUE)
                            print_colored(f"Currency: {country.get('currency', 'Unknown')}", Fore.BLUE)
                    else:
                        print_colored("[ERROR] BIN not found in database!", Fore.RED)
                except Exception as e:
                    print_colored(f"[ERROR] BIN lookup failed: {str(e)}", Fore.RED)
            else:
                print_colored("[ERROR] Invalid BIN format!", Fore.RED)
                
        elif choice == '11':
            if not generated_cards:
                print_colored("[ERROR] No cards generated yet!", Fore.RED)
                continue
                
            print_colored(f"\nYou have {len(generated_cards)} generated cards", Fore.CYAN)
            print_colored("1. Save as JSON", Fore.YELLOW)
            print_colored("2. Export as CSV", Fore.YELLOW)
            print_colored("3. Both", Fore.YELLOW)
            
            export_choice = input(f"\n{Fore.WHITE}Choose export format: {Style.RESET_ALL}").strip()
            
            if export_choice in ['1', '3']:
                filename = input(f"{Fore.WHITE}JSON filename (default: generated_cards.json): {Style.RESET_ALL}").strip()
                if not filename:
                    filename = "generated_cards.json"
                save_cards_to_file(generated_cards, filename)
                
            if export_choice in ['2', '3']:
                filename = input(f"{Fore.WHITE}CSV filename (default: generated_cards.csv): {Style.RESET_ALL}").strip()
                if not filename:
                    filename = "generated_cards.csv"
                export_cards_csv(generated_cards, filename)
                
        elif choice == '12':
            print_colored("Exiting credit card generator...", Fore.YELLOW)
            break
            
        else:
            print_colored("[ERROR] Invalid choice!", Fore.RED)
            continue
        
        if choice not in ['8', '11', '12']:
            continue_choice = input(f"\n{Fore.WHITE}Generate another card? (y/n): {Style.RESET_ALL}").strip().lower()
            if continue_choice != 'y':
                break

if __name__ == "__main__":
    run_credit_card_generator() 