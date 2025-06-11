# Prospect Identification

This project automates the extraction of LinkedIn users who have posted about recent promotions or new jobs, using browser automation and generative AI for data extraction.

## Project Details

- **Automates browser actions to search LinkedIn for posts about new jobs or promotions.**
- **Extracts user details (name, job title, company, location) from relevant posts.**
- **Outputs results to JSON files for further analysis or integration.**


## Setup & Usage

1. **Clone the repository and install dependencies.**
2. **Set up your environment variables in `.env` (Google API Key required).**
3. **Run the browser automation:**
    ```sh
    python Browser-Use-Implementation/browserUse.py
    ```
   This will create a `result.json` file with the extracted browser actions and raw data.

4. **Extract structured user data:**
    ```sh
    python Browser-Use-Implementation/extract_data.py
    ```
   This will generate `prospects.json` with the list of users and their details.