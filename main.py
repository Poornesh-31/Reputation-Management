from googleapiclient.discovery import build

# Replace with your actual API Key and Custom Search Engine ID
API_KEY = "AIzaSyDZdWWJTJOZEyn1V9XjV5_SnXaihDh9T-Y"  # Never share your API Key publicly!
SEARCH_ENGINE_ID = "34791939fbf6b48d0"
def get_search_results(query, num_results=5):
    """
    Perform a Google search using the API and return relevant results.

    Args:
        query (str): The search query (e.g., company name).
        num_results (int): Number of results to fetch.

    Returns:
        list: A list of dictionaries with 'title', 'snippet', and 'url'.
    """
    service = build("customsearch", "v1", developerKey=API_KEY)
    
    try:
        response = service.cse().list(q=query, cx=SEARCH_ENGINE_ID, num=min(num_results, 10)).execute()
        search_results = []
        
        for item in response.get("items", []):
            search_results.append({
                "title": item.get("title"),
                "snippet": item.get("snippet"),
                "url": item.get("link"),
            })
        
        return search_results
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def format_company_reputation(company_name):
    """
    Format the search results into a structured reputation summary.

    Args:
        company_name (str): The name of the company to search for.

    Returns:
        str: A structured summary of the company's reputation.
    """
    results = get_search_results(company_name, num_results=5)

    if not results:
        return f"No relevant information found for {company_name}."

    # Create a summary paragraph with relevant news and reviews
    paragraph = f"Latest reputation information about {company_name}:\n"

    for result in results:
        paragraph += f"\n- {result['title']}:\n  {result['snippet']}...\n  (Source: {result['url']})\n"

    return paragraph

# Example usage
if __name__ == "__main__":
    company_name = input("Enter the company name: ")
    result_text = format_company_reputation(company_name)

    print("\nCompany Reputation Summary:")
    print(result_text)
