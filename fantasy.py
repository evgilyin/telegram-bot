import requests
from bs4 import BeautifulSoup

def get_html(url):
	try:
		result = requests.get(url)
		result.raise_for_status()
		return result.text
	except(requests.RequestException, ValueError):
		return False

def get_info(html):
	html = get_html('https://www.sports.ru/fantasy/football/league/140288.html')
	if html:
		soup = BeautifulSoup(html, 'html.parser')
		div = soup.find('div', class_='stat mB6 players-rank').find('tbody')
		
		#Получаем данные каждой команды 1-5
		first = div.find_all('tr')[0]
		second = div.find_all('tr')[1]
		third = div.find_all('tr')[2]
		fourth = div.find_all('tr')[3]
		fifth = div.find_all('tr')[4]
		
		#Получаем номер позиции
		position_first = first.find('td').string
		position_second = second.find('td').string
		position_third = third.find('td').string
		position_fourth = fourth.find('td').string
		position_fifth = fifth.find('td').string

		#Получаем названия команд
		first_team_name = first.find('td', class_='name-td alLeft').string
		second_team_name = second.find('td', class_='name-td alLeft').string
		third_team_name = third.find('td', class_='name-td alLeft').string
		fourth_team_name = fourth.find('td', class_='name-td alLeft').string
		fifth_team_name = fifth.find('td', class_='name-td alLeft').string

		#Получаем ник игрока
		first_player_name = first.find('td', class_='name-td alLeft bordR small').find('strong').string
		second_player_name = second.find('td', class_='name-td alLeft bordR small').find('strong').string
		third_player_name = third.find('td', class_='name-td alLeft bordR small').find('strong').string
		fourth_player_name = fourth.find('td', class_='name-td alLeft bordR small').find('strong').string
		fifth_player_name = fifth.find('td', class_='name-td alLeft bordR small').find('strong').string

		#Получаем очки тура
		first_tour_scores = first.find_all('td')[4].string
		second_tour_scores = second.find_all('td')[4].string
		third_tour_scores = third.find_all('td')[4].string
		fourth_tour_scores = fourth.find_all('td')[4].string
		fifth_tour_scores = fifth.find_all('td')[4].string

		#Получаем общие очки
		first_overall_scores = first.find_all('td')[5].string
		second_overall_scores = second.find_all('td')[5].string
		third_overall_scores = third.find_all('td')[5].string
		fourth_overall_scores = fourth.find_all('td')[5].string
		fifth_overall_scores = fifth.find_all('td')[5].string

		# return(position_first, position_second, position_third, position_fourth, position_fifth, first_team_name, second_team_name, third_team_name, fourth_team_name, fifth_team_name, first_player_name, second_player_name, third_player_name, fourth_player_name, fifth_player_name, first_tour_scores, second_tour_scores, third_tour_scores, fourth_tour_scores, fifth_tour_scores, first_overall_scores, second_overall_scores, third_overall_scores, fourth_overall_scores, fifth_overall_scores)

		return(f'{position_first} - {first_team_name} / {first_player_name} - {first_tour_scores} - {first_overall_scores}\n{position_second} - {second_team_name} / {second_player_name} - {second_tour_scores} - {second_overall_scores}\n{position_third} - {third_team_name} / {third_player_name} - {third_tour_scores} - {third_overall_scores}\n{position_fourth} - {fourth_team_name} / {fourth_player_name} - {fourth_tour_scores} - {fourth_overall_scores}\n{position_fifth} - {fifth_team_name} / {fifth_player_name} - {fifth_tour_scores} - {fifth_overall_scores}')


# if __name__ == "__main__":
# 	html = get_html('https://www.sports.ru/fantasy/football/league/140288.html')
# 	if html:
# 		get_info(html)
