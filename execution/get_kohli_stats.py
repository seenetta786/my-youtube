import requests
from bs4 import BeautifulSoup
import json
from googlesearch import search

def get_kohli_stats():
    player_name = "Virat Kohli"
    query = f"{player_name} cricbuzz"
    profile_link = None
    try:
        search_url = f"https://duckduckgo.com/html/?q={query}"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", class_="result__url")
        for link in links:
            href = link.get("href")
            if "cricbuzz.com/profiles/" in href:
                profile_link = href
                print(f"Found profile: {profile_link}")
                break
        if not profile_link:
            print("No player profile found")
            return
    except Exception as e:
        print(f"Search failed: {str(e)}")
        return
    except Exception as e:
        print(f"Search failed: {str(e)}")
        return
    
    # Get player profile page
    c = requests.get(profile_link).text
    soup = BeautifulSoup(c, "lxml")
    
    # Name, country and image
    name_country_div = soup.find("div", class_="cb-col cb-col-100 cb-bg-white")
    name = name_country_div.find("h1", class_="cb-font-40").text
    country = name_country_div.find("h3", class_="cb-font-18 text-gray").text
    image_url = None
    images = name_country_div.findAll('img')
    for image in images:
        image_url = image['src']
        break  # Just get the first image

    # Personal information and rankings
    personal_info_divs = soup.find_all("div", class_="cb-col cb-col-60 cb-lst-itm-sm")
    role = personal_info_divs[2].text.strip()
    
    icc_rankings_divs = soup.find_all("div", class_="cb-col cb-col-25 cb-plyr-rank text-right")
    # Batting rankings
    test_bat_rank = icc_rankings_divs[0].text.strip()
    odi_bat_rank = icc_rankings_divs[1].text.strip()
    t20_bat_rank = icc_rankings_divs[2].text.strip()
    
    # Bowling rankings
    test_bowl_rank = icc_rankings_divs[3].text.strip()
    odi_bowl_rank = icc_rankings_divs[4].text.strip()
    t20_bowl_rank = icc_rankings_divs[5].text.strip()

    # Summary of the stats
    summary_divs = soup.find_all("div", class_="cb-plyr-tbl")
    batting_summary = summary_divs[0]
    bowling_summary = summary_divs[1]

    # Batting statistics
    bat_rows = batting_summary.find("tbody").find_all("tr")
    batting_stats = {}
    for row in bat_rows:
        cols = row.find_all("td")
        format_name = cols[0].text.strip().lower()
        batting_stats[format_name] = {
            "matches": cols[1].text.strip(),
            "runs": cols[3].text.strip(),
            "highest_score": cols[5].text.strip(),
            "average": cols[6].text.strip(),
            "strike_rate": cols[7].text.strip(),
            "hundreds": cols[12].text.strip(),
            "fifties": cols[11].text.strip(),
        }

    # Bowling statistics
    bowl_rows = bowling_summary.find("tbody").find_all("tr")
    bowling_stats = {}
    for row in bowl_rows:
        cols = row.find_all("td")
        format_name = cols[0].text.strip().lower()
        bowling_stats[format_name] = {
            "balls": cols[3].text.strip(),
            "runs": cols[4].text.strip(),
            "wickets": cols[5].text.strip(),
            "best_bowling_innings": cols[9].text.strip(),
            "economy": cols[7].text.strip(),
            "five_wickets": cols[11].text.strip(),
        }

    # Create player stats dictionary
    player_data = {
        "name": name,
        "country": country,
        "image": image_url,
        "role": role,
        "rankings": {
            "batting": {
                "test": test_bat_rank,
                "odi": odi_bat_rank,
                "t20": t20_bat_rank
            },
            "bowling": {
                "test": test_bowl_rank,
                "odi": odi_bowl_rank,
                "t20": t20_bowl_rank
            }
        },
        "batting_stats": batting_stats,
        "bowling_stats": bowling_stats
    }

    # Save to JSON for inspection
    with open("kohli_stats.json", "w", encoding="utf-8") as f:
        json.dump(player_data, f, indent=4, ensure_ascii=False)
    
    print("Successfully scraped data and saved to kohli_stats.json")

if __name__ == "__main__":
    get_kohli_stats()