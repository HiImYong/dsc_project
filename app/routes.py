import copy
import json
import math
import random
from sympy import symbols, Eq, solve
from flask import jsonify, render_template, request
from app import app
from app.models import User
import numpy as np


class Player:
    def __init__(self, 이름, 레벨, 팀, 게임수):
        self.이름 = 이름
        self.레벨 = 레벨
        self.팀 = 팀
        self.게임수 = 게임수


@app.route('/users')
def users():
	# users 데이터를 Json 형식으로 반환한다
    return {"members": [{ "id" : 1, "name" : "yerin" },
    					{ "id" : 2, "name" : "dalkong" }]}
                   
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/result/', methods=['GET'])
def result():
    data = request.args.get('data')

    parsed_data = data.split(', ')
    users = []

    print(data)
    print(type(data))
    # users = User.query.filter_by(name='유용재').first()

    for input_user in parsed_data:
        try:
            user = User.query.filter_by(name=input_user).first()
            if user is not None:
                users.append(user)
                print(f"사용자 이름: {user.name}")
            else:
                msg = f"'{input_user}' 데이터는 존재하지 않습니다."
                print(msg)
                return msg
        except Exception as e:
            print(e)

    print('유저목록 : ', users)
    random.shuffle(users)

    user_cnt = len(users)

    """
    레벨구획화(추후 진행)
    user_level_3 = 0
    user_level_2 = 0
    user_level_1 = 0

    for user in users:
        if user.level == '3':
            user_level_3 += 1
        elif user.level == '2':
            user_level_2 += 1
        elif user.level == '1':
            user_level_1 += 1

    blue_team_cnt_3 = 0
    blue_team_cnt_2 = 0
    blue_team_cnt_1 = 0

    red_team_cnt_3 = 0
    red_team_cnt_2 = 0
    red_team_cnt_1 = 0

    devide_team_3 = None
    devide_team_2 = None

    if user_level_3 % 2 != 0:
        blue_team_cnt_3 = math.ceil(user_level_3/2)
        devide_team_3 = 'ceil'
    else:
        blue_team_cnt_3 = user_level_3/2
    red_team_cnt_3 = user_level_3 - blue_team_cnt_3

    if user_level_2 % 2 != 0 and devide_team_3 == 'ceil':
        blue_team_cnt_2 = math.floor(user_level_2/2)
        devide_team_2 = 'floor'
    elif user_level_2 % 2 != 0:
        blue_team_cnt_2 = math.ceil(user_level_2/2)
        devide_team_2 = 'ceil'
    else:
        blue_team_cnt_2 = user_level_2/2
    red_team_cnt_2 = user_level_2 - blue_team_cnt_2

    if user_level_1 % 2 != 0 and devide_team_2 == 'ceil':
        blue_team_cnt_1 = math.floor(user_level_1/2)
    elif user_level_1 % 2 != 0 or devide_team_2 == 'floor':
        blue_team_cnt_1 = math.ceil(user_level_1/2)
    else:
        blue_team_cnt_1 = user_level_1/2
    red_team_cnt_1 = user_level_1 - blue_team_cnt_1
    """
    

    # 팀카운트 디버깅
    tournament_mtx = np.empty((6, 3), dtype=object)

    for row in range(6):
        for col in range(3):
            tournament_mtx[row, col] = []

    # total_sum_game = 0

    blue_red_buffer = 0

    all_red_cnt = 0
    all_blue_cnt = 0

    all_player_info = []

    for idx, user in enumerate(users, start=1):
        player_name = f"player_{idx}"

        if blue_red_buffer == 0:
            team = '청'  # 37
            globals()[player_name] = Player(user.name, user.level, team, 0)
            player_ins = globals().get(player_name)
            all_player_info.append(vars(player_ins))
            all_blue_cnt += 1

        else:
            team = '홍'  # 35
            globals()[player_name] = Player(user.name, user.level, team, 0)
            player_ins = globals().get(player_name)
            all_player_info.append(vars(player_ins))
            all_red_cnt += 1

        if blue_red_buffer == 0:
            blue_red_buffer = 1
        else:
            blue_red_buffer = 0

    biggerTeam = ''
    홍버퍼 = 36
    청버퍼 = 36

    # if all_blue_cnt > all_red_cnt:
    #     biggerTeam = '청'
    #     홍버퍼 = 35
    #     청버퍼 = 37

    # elif all_blue_cnt < all_red_cnt:
    #     biggerTeam = '홍'
    #     홍버퍼 = 37
    #     청버퍼 = 35
    # elif all_blue_cnt == all_red_cnt:
    #     biggerTeam = '동'
    #     홍버퍼 = 36
    #     청버퍼 = 36

    a, b = symbols('a b')

    blue_equation1 = ''
    red_equation1 = ''

    blue_big_game = 0
    blue_small_game = 0

    red_big_game = 0
    red_small_game = 0    

    print('>> 총 유저 수 ::', user_cnt)

    """
    사람 수는 먼저 반으로 나눠진다
    청, 홍팀 사람 수로 연립방정식을 하다보니, 빅게임 스몰게임이 필요했다.
    처음에 빅게임 스몰게임을 막 넣어주다보니 7을 기준으로 5-4에서 6-5로 바뀐다.
    규칙을 찾아보니 청팀, 홍팀수로 청, 홍팀의 게임 수로 나눠줘야 하더라.
    36/청
    36/홍
    나눈 수로 빅, 스몰을 올림 내림 잡자주자.

        소수점계산 = 72/user_cnt
    big_game = math.ceil(소수점계산)
    small_game = math.floor(소수점계산)
    """

    # 소수점계산 = 72/user_cnt
    # blue_big_game = math.ceil(소수점계산)
    # blue_small_game = math.floor(소수점계산)

    
    # red_big_game = math.ceil(소수점계산)
    # red_small_game = math.floor(소수점계산)

    블루소수점계산 = 36/all_blue_cnt
    blue_big_game = math.ceil(블루소수점계산)
    blue_small_game = math.floor(블루소수점계산)
    print('~~~~~')
    print(all_blue_cnt)
    print(blue_big_game)
    print(blue_small_game)

    print('!!')
    레드소수점계산 = 36/all_red_cnt
    red_big_game = math.ceil(레드소수점계산)
    red_small_game = math.floor(레드소수점계산)    
    print(all_red_cnt)
    print(red_big_game)
    print(red_small_game)

    


    # 연립방정식
    blue_equation1 = Eq(blue_big_game*a + blue_small_game*b, 청버퍼)    
    blue_equation2 = Eq(a + b, all_blue_cnt)
    blue_solution = solve((blue_equation1, blue_equation2), (a, b))

    if b not in blue_solution:
        temp = blue_solution[a]
        blue_solution[a] = temp + b
        blue_solution[b] = 0


    red_equation1 = Eq(red_big_game*a + red_small_game*b, 홍버퍼)
    red_equation2 = Eq(a + b, all_red_cnt)
    red_solution = solve((red_equation1, red_equation2), (a, b))

    if b not in red_solution:
        temp = red_solution[a]
        red_solution[a] = temp + b
        red_solution[b] = 0    

    print('방정식의 해')
    print(blue_solution)
    print(red_solution)

    blue_big = blue_solution[a]
    blue_small = blue_solution[b]
    red_big = red_solution[a]
    red_small = red_solution[b]

    print('방정식 변수 이동')
    print(blue_big)
    print(blue_small)
    print(red_big)
    print(red_small)


    청팀인원카운트용 = copy.deepcopy(all_blue_cnt)
    홍팀인원카운트용 = copy.deepcopy(all_red_cnt)

    print(청팀인원카운트용)
    print(홍팀인원카운트용)

    # 인원당 게임수
    # three_game = user_cnt*4 - 72 # 답으로 나오는 n명은 3게임

    for player in all_player_info:

        해당선수의게임수 = 0

        print(player)
        print('.....')

        if player['팀'] == '청' and 청팀인원카운트용 != 0:

            if blue_small > 0 and 청팀인원카운트용 == blue_small and blue_small != 0:
                해당선수의게임수 = blue_small_game
                blue_small -= 1
                청팀인원카운트용 -= 1
                

            elif blue_small > 0 and blue_big > 0:
                해당선수의게임수 = random.choice([blue_big_game, blue_small_game])
                if 해당선수의게임수 == blue_small_game:
                    # three_game -= 1
                    blue_small -= 1
                    청팀인원카운트용 -= 1
                elif 해당선수의게임수 == blue_big_game:
                    # three_game -= 1
                    blue_big -= 1
                    청팀인원카운트용 -= 1

            elif blue_small == 0 and blue_big > 0:
                해당선수의게임수 = blue_big_game
                청팀인원카운트용 -= 1
                blue_big -= 1
            
            

        if player['팀'] == '홍' and 홍팀인원카운트용 != 0:

            if red_small > 0 and 홍팀인원카운트용 == red_small and red_small != 0:
                해당선수의게임수 = red_small_game
                red_small -= 1
                홍팀인원카운트용 -= 1

            elif red_small > 0 and red_big > 0:
                해당선수의게임수 = random.choice([red_big_game, red_small_game])
                if 해당선수의게임수 == red_small_game:
                    # three_game -= 1
                    red_small -= 1
                    홍팀인원카운트용 -= 1
                elif 해당선수의게임수 == red_big_game:
                    # three_game -= 1
                    red_big -= 1
                    홍팀인원카운트용 -= 1

            elif red_small == 0:
                해당선수의게임수 = red_big_game
                홍팀인원카운트용 -= 1
                red_big -= 1

        player['게임수'] = 해당선수의게임수
        print('해당선수의게임수 >> ', 해당선수의게임수)

    sorted_all_players_2 = sorted(all_player_info, key=lambda x: x['팀'])

    check_final_man = 0

    row_cnt = [12, 12, 12, 12, 12, 12]


    # print('>> 랜덤배치 시작')
    # print(sorted_all_players_2)
    for player in sorted_all_players_2:

        game_circuit_cnt = player['게임수']
        check_final_man += 1

        while game_circuit_cnt > 0:
            row = np.random.randint(6)
            col = np.random.randint(3)

            max_value = np.max(row_cnt)
            max_positions = []

            for i in range(6):
                if row_cnt[i] == max_value:
                    max_positions.append(i)

            if row not in max_positions:
                continue

            found = False
            current_list = tournament_mtx[row, col]
            current_cnt = len(current_list)

            if current_cnt == 4:
                continue
            # print('------------------')
            # print(sorted_all_players_2)
            # print('총원')
            # print(user_cnt)
            # print('블루팀총원 > ', all_blue_cnt)
            # print('레드팀총원 > ', all_red_cnt)

            # print(청팀인원카운트용)
            # print(홍팀인원카운트용)
            # print('카운트마이너스')
            # print('파', blue_small)
            # print('빨', red_small)
            # print('파', blue_big)
            # print('빨', red_big)
            # print(row_cnt)
            # print('초기게임수')
            # print('파', all_blue_cnt)
            # print('파', blue_big_game)
            # print('파', blue_small_game)
            # print('빨', all_red_cnt)
            # print('빨', red_big_game)
            # print('빨', red_small_game)    
            # print('방정식의 해')
            # print('파', blue_solution)            
            # print('빨', red_solution)

            # print('현재 행렬 >> ', row, ' / ', col)
            # print('player >>> ', player)
            # print(tournament_mtx)
            red_cnt = 0
            blue_cnt = 0

            for item in current_list:
                # print(item)
                if item['팀'] == '홍':
                    red_cnt += 1
                if item['팀'] == '청':
                    blue_cnt += 1

            if player['팀'] == '홍':
                if red_cnt == 2:
                    # print('홍이 더 많거나 이미 다 참')
                    continue

            if player['팀'] == '청':
                if blue_cnt == 2:
                    # print('청이 더 많거나 이미 다 참')
                    continue

            # 플레이어 정보 확인 여부를 나타내는 변수

            for col_cnt in range(len(tournament_mtx[row])):

                item = tournament_mtx[row][col_cnt]  # 해당 행의 3열을 돌면서~
                for info in item:
                    if info['이름'] == player['이름']:  # 해당 열의 이름을 비교한다~
                        found = True
                        break  # 이미 해당 플레이어가 매트릭스에(행에) 있어서 해당 행은 건너뛰고자 합니다.
                    if found == True:
                        break  # 이미 해당 플레이어가 매트릭스에(행에) 있어서 해당 행은 건너뛰고자 합니다.
                if found == True:
                    break      # 이미 해당 플레이어가 매트릭스에(행에) 있어서 해당 행은 건너뛰고자 합니다.

            if found == True:  # 이미 해당 플레이어가 매트릭스에(행에) 있어서 해당 행은 건너뛰고자 합니다.

                continue

            if current_cnt < 4:
                current_list.append(player)
                game_circuit_cnt -= 1

                row_cnt[row] = row_cnt[row] - 1

    arr_as_list = tournament_mtx.tolist()
    # print(arr_as_list)
    json_data = json.dumps(arr_as_list, ensure_ascii=False)

    return jsonify(json_data)
