import requests
import hashlib
import time

def check_email_breach(email):
    """
    Checks if an email address has been breached using the Have I Been Pwned (HIBP) API.

    Args:
        email: The email address to check.

    Returns:
        A list of breach details if the email is found, or None if not found.
    """
    try:
        # Hash the email's prefix using SHA-1 (HIBP API requirement)
        email_hash = hashlib.sha1(email.encode('utf-8')).hexdigest().upper()
        prefix = email_hash[:6]
        suffix = email_hash[6:]

        # HIBP API endpoint
        url = f"https://api.pwnedpasswords.com/range/{prefix}"

        # Make the API request
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        # Parse the response
        hashes = response.text.splitlines()

        # Check for a match
        for h in hashes:
            h_suffix, count = h.split(':')
            if h_suffix == suffix:
                # Retrieve breach data from pwnedbreaches endpoint
                breach_url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
                headers = {'User-Agent': 'DataBreachChecker'} #Required by the Api
                breach_response = requests.get(breach_url, headers=headers)
                if breach_response.status_code == 200:
                    return breach_response.json()
                elif breach_response.status_code == 404:
                    return None #email not found on breach database.
                else:
                    print(f"Error retrieving breach details: {breach_response.status_code}")
                    return None

        return None  # Email not found in the hashed range

    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        return None
    except ValueError as e:
        print(f"Error parsing API response: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def main():
    """
    Main function to get user input and check for breaches.
    """
    email = input("Enter your email address: ")

    if not email:
        print("Email cannot be empty.")
        return

    print("Checking for breaches...")
    breaches = check_email_breach(email)

    if breaches:
        print(f"\nYour email '{email}' has been found in the following data breaches:")
        for breach in breaches:
            print(f"- {breach['Title']} ({breach['BreachDate']}): {breach['Description'].replace('<p>', '').replace('</p>', '')}")
            print(f"  Compromised data: {', '.join(breach['DataClasses'])}")
            print(f"  More info: {breach['Domain']}")
            print("-" * 20)

    else:
        print(f"\nYour email '{email}' has not been found in any known data breaches (or is not in the pwnedbreaches database).")

if __name__ == "__main__":
    main()






    