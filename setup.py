from utils import *

def show_menu():
    '''
    Shows input choices.
    '''
    print(" Bloom Filter Pipeline\n")
    print("1. Process data (CSV → JSON + Filter malicious links)")
    print("2. Populate Bloom Filter")
    print("3. Check Accuracy")
    print("4. Exit\n\n")


def run_choice(choice):
    '''
    Calls function depending on what choice was made.
    '''
    if choice == "1":
        print("\n[STEP] Processing dataset...")
        csv_to_json()
        filter_malicious_webpages()

    elif choice == "2":
        print("\n[STEP] Populating Bloom Filter...")
        populate_bloom_filter()

    elif choice == "3":
        print("\n[STEP] Checking accuracy...")
        check_accuracy()

    elif choice == "4":
        print("Exiting...")
        return False

    else:
        print("Invalid option. Please choose 1–4.")

    return True


def main():
    '''
    Runs menu until user decides to exit. 
    '''
    running = True

    while running:
        show_menu()
        choice = input("Select an option (1–4): ").strip()
        running = run_choice(choice)


if __name__ == "__main__":
    main()