from googlesearch import search
import requests
from bs4 import BeautifulSoup

def get_search_results(query, num_results=5):
    """
    Perform a Google search and return relevant results without an API key.
    
    Args:
        query (str): The search query (e.g., company name).
        num_results (int): Number of results to fetch.
        
    Returns:
        list: A list of dictionaries with 'title' and 'snippet' of search results.
    """
    search_results = []
    try:
        for url in search(query, num_results=num_results):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Attempt to extract meaningful content from articles or main text bodies
            title = soup.title.string if soup.title else "No title"
            
            # Attempt to extract the first meaningful paragraph or article content
            paragraphs = soup.find_all('p')
            content = ''
            for p in paragraphs:
                content += p.get_text().strip()
            
            # Limit content length and avoid unwanted sections
            snippet = content[:300]  # Adjust the length as needed

            # Filter out non-relevant content
            if len(snippet) > 50 and not any(keyword in snippet.lower() for keyword in ["click here", "contact", "about", "what we do"]):
                search_results.append({
                    'title': title,
                    'snippet': snippet,
                    'url': url
                })
        return search_results
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def format_company_reputation(company_name):
    """
    Format the results into a structured summary focusing on achievements and reputation.
    
    Args:
        company_name (str): The name of the company to search for.
        
    Returns:
        str: A structured summary paragraph for the company.
    """
    results = get_search_results(company_name, num_results=5)
    
    if not results:
        return f"No relevant information found for {company_name}."

    # Create a summary paragraph with relevant achievements and news
    paragraph = f"Latest information about {company_name}:\n"
    
    for result in results:
        paragraph += f"\n- {result['title']}:\n  {result['snippet']}...\n"
    
    return paragraph

# Example usage
if __name__ == "__main__":
    company_name = input("Enter the company name: ")
    result_text = format_company_reputation(company_name)
    
    print("\nCompany Reputation Summary:")
    print(result_text)