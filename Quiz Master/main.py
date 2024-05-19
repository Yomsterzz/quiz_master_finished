import pgzrun

TITLE = "Quiz Master"
WIDTH = 870
HEIGHT = 650

question_box = Rect(0,0,650,150)
marquee_box = Rect(0,0,880,80)
timer_box = Rect(0,0,150,150)
skip_box = Rect(0,0,150,330)
answer_box1 = Rect(0,0,300,150)
answer_box2 = Rect(0,0,300,150)
answer_box3 = Rect(0,0,300,150)
answer_box4 = Rect(0,0,300,150)

score = 0
time_left = 10
question_file_name = "questions.txt"
marquee_msg = ""
is_game_over = False
answer_boxes = [answer_box1, answer_box2, answer_box3, answer_box4]
questions = []
question_count = 0
question_index = 0
question = ""

marquee_box.move_ip(0,0)
question_box.move_ip(20,100)
timer_box.move_ip(700,100)
answer_box1.move_ip(20,270)
answer_box2.move_ip(370,270)
answer_box3.move_ip(20,450)
answer_box4.move_ip(370,450)
skip_box.move_ip(700,270)

def draw():
    global marquee_msg
    screen.clear()
    screen.draw.filled_rect(marquee_box, "black")
    screen.draw.filled_rect(question_box, "blue")
    screen.draw.filled_rect(timer_box, "blue")
    screen.draw.filled_rect(skip_box, "green")

    for answerbox in answer_boxes:
        screen.draw.filled_rect(answerbox, "orange")
    
    marquee_msg = "Welcome to the quiz game!"
    marquee_msg = marquee_msg + " Question {} of {}".format(question_index, question_count)
    screen.draw.textbox(marquee_msg, marquee_box, color="white")
    screen.draw.textbox("SKIP", skip_box, color="white", shadow=(0.5,0.5), scolor="dim grey", angle=-90)
    screen.draw.textbox(str(time_left), timer_box, color="white", shadow=(0.5,0.5), scolor="dim grey")
    screen.draw.textbox(question[0].strip(), question_box, color="white", shadow=(0.5,0.5), scolor="dim grey")

    index = 1
    for box in answer_boxes:
        screen.draw.textbox(question[index].strip(), box, color="white", shadow=(0.5,0.5), scolor="dim grey")
        index += 1

def update():
    move_marquee()

def move_marquee():
    marquee_box.x = marquee_box.x+2
    if marquee_box.right < 0:
        marquee_box.left = WIDTH

def read_question_file():
    global question_count, questions
    question_file = open(question_file_name, "r")
    for line in question_file:
        questions.append(line)
        question_count += 1
    
    question_file.close()

def read_next_question():
    global question_index

    question_index += 1
    return questions.pop(0).split(",")

def on_mouse_down(pos):
    index = 1
    for box in answer_boxes:
        if box.collidepoint(pos):
            if index is int(question[5]):
                correct_answer()
            else:
                game_over()
        index += 1
    if skip_box.collidepoint(pos):
        skip_question()

def correct_answer():
    global question, time_left, score, questions
    score += 1
    if questions:
        question = read_next_question()
        time_left = 10
    else:
        game_over()

def skip_question():
    global question, time_left
    if questions and not is_game_over:
        question = read_next_question()
        time_left = 10
    else:
        game_over()

def game_over():
    global question, time_left, is_game_over, message
    message = f"Game over. \n You scored {score} out of {question_count}."
    question = [message, " - ", " - ", " - ", " - ", 5]
    time_left = 0
    is_game_over = True

def update_timer():
    global time_left
    if time_left:
        time_left -= 1
    else:
        game_over()

read_question_file()
question = read_next_question()
clock.schedule_interval(update_timer, 1)

pgzrun.go()