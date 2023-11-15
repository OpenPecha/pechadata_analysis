import csv
import os
import random

from github import Github


def select_random_pecha_ids(csv_file_path, num_rows):
    try:
        selected_pecha_ids = []

        with open(csv_file_path, newline="", encoding="utf-8") as csvfile:
            csv_reader = csv.DictReader(csvfile)
            all_rows = list(csv_reader)

            # Check if the number of rows requested is greater than the total number of rows
            if num_rows > len(all_rows):
                num_rows = len(all_rows)

            # Randomly select num_rows from the list of all rows
            selected_rows = random.sample(all_rows, num_rows)

            # Extract the Pecha IDs from the selected rows
            for row in selected_rows:
                pecha_id = row["Pecha ID"].strip()
                selected_pecha_ids.append(pecha_id)

        return selected_pecha_ids  # Ensure that the list of Pecha IDs is returned
    except Exception as e:
        print(f"Error in select_random_pecha_ids: {e}")
        return None


def extract_and_save_text_files(
    organization, github_token, pecha_ids, start_offset, end_offset, output_folder
):
    try:
        # Initialize the PyGithub client with your token
        g = Github(github_token)

        # Get the organization
        org = g.get_organization(organization)

        for pecha_id in pecha_ids:
            # Assuming the GitHub repository name matches the Pecha ID
            repo_name = pecha_id

            try:
                # Get the repository within the organization
                repo = org.get_repo(repo_name)

                # Construct the base folder path within the repository
                base_folder_path = f"{pecha_id}.opf/base"

                # Get the contents of the base folder
                base_folder_contents = repo.get_contents(base_folder_path)

                # Iterate through the contents and process text files
                for file_content in base_folder_contents:
                    if file_content.type == "file" and file_content.name.endswith(
                        ".txt"
                    ):
                        # Decode the content to get the text
                        full_text = file_content.decoded_content.decode(
                            "utf-8", errors="replace"
                        )

                        # Extract the desired text range
                        extracted_text = full_text[start_offset:end_offset]

                        # Create the output folder if it doesn't exist
                        os.makedirs(output_folder, exist_ok=True)

                        # Construct the output file path
                        output_file_path = os.path.join(
                            output_folder, f"{pecha_id}_{file_content.name}"
                        )

                        # Write the extracted text to the output file
                        with open(
                            output_file_path, "w", encoding="utf-8"
                        ) as output_file:
                            output_file.write(extracted_text)

                        print(
                            f"Extracted and saved text from {file_content.path} to {output_file_path}"
                        )
            except Exception as e:
                print(f"Error in accessing repository {repo_name}: {e}")

    except Exception as e:
        print(f"Error in extract_and_save_text_files: {e}")


if __name__ == "__main__":
    # Your GitHub personal access token (replace with your actual token)
    github_token = "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"
    # Example usage:
    organization_name = "OpenPecha-Data"

    # Example usage:
    csv_file_path = "../../data/opf_catalog.csv"
    num_rows_to_select = 50
    start_offset = 1500
    end_offset = 3000
    output_folder = "../../data/output"  # Folder to save the extracted text files

    selected_pecha_ids = select_random_pecha_ids(csv_file_path, num_rows_to_select)
    if selected_pecha_ids:
        print("Randomly selected Pecha IDs:")
        for pecha_id in selected_pecha_ids:
            print(pecha_id)

        extract_and_save_text_files(
            organization_name,
            github_token,
            selected_pecha_ids,
            start_offset,
            end_offset,
            output_folder,
        )
    else:
        print("No Pecha IDs were selected.")
