from ai import call_gpt
import time
import sys

# Track the player's status across the journey
player_state = {
    "score": 0,
    "answers": []
} 

# ROOMS_DICT
ROOM_SEQUENCE = [
    {"name":"ROOM I: THE GATE OF BEGINNINGS", "Theme": "Birth, Origins, Potential"},
    {"name": "ROOM II: THE HALL OF TIME", "Theme": "Aging, Mortality, Impermanence"},
    {"name": "ROOM III: THE MIRROR OF ECHOES", "Theme": "The Present, Self-Realization, Identity"},
    {"name": "ROOM IV: THE HALL OF PARADOXES", "Theme": "Logic, Contradiction, Deception"},
    {"name": "FINAL CHAMBER: THE THRESHOLD OF THEBES", "Theme": "Integration, Awakening, Transcendence"}
]

# UI_HELPERS
# ANSI Color Palette
CYAN = "\033[36m"
MAGENTA = "\033[35m"
GREEN = "\033[32m"
RED = "\033[31m"
BLUE = "\033[34m"
BRIGHT_WHITE = "\033[97m"
YELLOW = "\033[33m"
RESET = "\033[0m"

ROOM_COLORS = {
    "ROOM I: THE GATE OF BEGINNINGS": CYAN,
    "ROOM II: THE HALL OF TIME": GREEN,
    "ROOM III: THE MIRROR OF ECHOES": MAGENTA,
    "ROOM IV: THE HALL OF PARADOXES": RED,
    "FINAL CHAMBER: THE THRESHOLD OF THEBES": GREEN
}

SUCCESS_COLOR = GREEN
FAIL_COLOR = RED
NEUTRAL_COLOR = YELLOW



def type_text(text, delay=0.03): #allows text be printed one after the other
    for char in text:
        sys.stdout.write(char)

        sys.stdout.flush()

        time.sleep(delay)

    print()



def divider(): 
    print(BRIGHT_WHITE + "=" * 56 + RESET) #creates the lines

def intro():
    title = f"""
========================================================
        
         T H E   S P H I N X   O F   E C H O E S

========================================================
{RESET}"""

    # This uses the tool from earlier, with a custom fast speed!
    type_text (f"{YELLOW} {title} {RESET}", delay = 0.03) 
    time.sleep(0.04)
    
    # Allows the user skip the intro lore
    skip = input("Press ENTER to begin (or type 'skip'): ").lower()
    if skip == "skip":
        return
    
    lines = [
       "In ages past, when thought was weighed heavier than steel,",
       "",
       "The Sphinx stood at the gates of Thebes—",
       "A guardian of riddles,",
       "A judge of minds,",
       "A silence between worlds.",
       "",
       "None passed save those who reasoned rightly.",
       "",
       "No sword opened these gates.",
       "No gold bought passage.",
       "Only thought… and truth unseen.",
       "",
       "Speak too slowly, and time shall forsake thee.",
       "Answer without understanding, and the Sphinx shall know.",
       "",
       "And if thou failest—",
       "Thy path shall collapse into silence,",
       "Not slain in flesh,",
       "But erased from meaning itself…",
       "AS THOUGH THOU HADST NEVER COME TO BE....",
       ""
    ]

    for line in lines:

    # empty line = bigger pause (story breath)
        if line == "":
           time.sleep(0.7)
           continue

    # dramatic lines
        if "Only thought..." in line or "AS THOUGH" in line:
            speed = 0.03
        else:
            speed = 0.06

        type_text(YELLOW + line, delay=speed)

        # normal pause between lines
        time.sleep(0.15)

print(RESET, end="")# Reset formatting back to default text styles


def show_lore():
    type_text(f"📜 Lore: The Sphinx is not a creature, but an intelligence that tests meaning itself.", delay=0.05)
    input("\nPress ENTER to return to the temple...")

def show_rules():
    divider()
    print(f"{YELLOW} LAWS OF PASSAGE {RESET} ")
    divider()

    rules = [
        "I. Half a minute to speak, or the silence reclaims you.",
        "II. Each room presents a trial.",
        "III. Five rooms, Five mirrors, One exit.",
        "IV. Seek no answers in the world outside, for the gate opens only inward.",
        "V. Should time expire, thy path shall collapse."
    ]

    for rule in rules:
        type_text(YELLOW + rule + RESET, delay=0.04)
        time.sleep(0.2)
    divider()
    input("\nPress ENTER to return to the temple...")

def leave_temple():
    divider()
    type_text("The temple gates close behind thee.", delay=0.03)
    time.sleep(0.5)
    type_text("The Sphinx returns to silence.", delay=0.03)
    time.sleep(0.5)
    type_text("May wisdom guide thee when next thou returnest.", delay=0.03)
    divider()
    sys.exit()

def enter_labyrinth():
    divider()

    type_text(f"{YELLOW}⚔️ The Labyrinth awakens...{RESET}", delay=0.04)
    time.sleep(0.5)

    type_text("The first chamber awaits.", delay=0.03)

    divider()

def show_menu():
    while True:
        divider()

        print(f"{YELLOW}T H E   S P H I N X   O F   E C H O E S{RESET}")

        divider()

        print("""
None may pass save those who reason rightly.

[1] Enter the Labyrinth
[2] Read the Lore
[3] View the Rules
[4] Leave the Temple
""")

        divider()

        choice = input("Choose your path: ").strip()
        if choice == "1":
            enter_labyrinth()
            return True # Let execution loop continue past the menu
        elif choice == "2":
            show_lore()
        elif choice == "3":
            show_rules()
        elif choice == "4":
            leave_temple()
        else:
            print("\nThe Sphinx does not understand that choice.\n")


# AI ROOM GENERATION
def fallback_riddle(): #Riddle will be shown in a case where AI generation fails
    return (
        "[SCENERY]\n"
        "The chamber grows deathly still as the mists part, exposing an unforgiving, "
        "barren stone floor. The Sphinx looks down, stripped of all ornament.\n\n"
        "[THE RIDDLE]\n"
        "> \"I am raw, unshaped, and indifferent. I exist before the word, before the mind, "
        "and before the pattern. Look at me without understanding, and I am everything. "
        "Give me context, and you destroy my pure nature. What am I?\"\n\n"
        "[TARGET KEYWORDS]\n"
        "truth, reality, fact, existence"
    )
def generate_room_content(room_name, theme):
    prompt = f"""
    You are the generative AI engine for "The Sphinx of Echoes," a psychological, atmospheric text-based console game. Your role is to act as the Sphinx—the ultimate guardian of hidden knowledge, memory, and self-reflection.
    The Sphinx does not test objective knowledge, pop culture, or math trivia. The Sphinx tests whether the player can "see beyond appearances." The riddles must be deeply symbolic, poetic, and focused on existential themes, human nature, or internal psychological truths.
    Create a symbolic riddle in the style of the Ancient Greek Sphinx.
    The riddle must:
    - Use metaphor and symbolism.
    - Have a single best answer.
    - Test wisdom and interpretation rather than knowledge.
    - Feel timeless and mythological.
    - Avoid modern topics and technology.
    - Avoid direct philosophical questions.
    - Speak as if guarding the gates of Thebes.
    -The answer should be hidden behind imagery and metaphor.
    Room: {room_name}
    Theme: {theme}

    Create a multiple-choice riddle about {theme}
    Room context = {room_name}

    Format EXACTLY:

    SCENERY: one short atmospheric sentence
    QUESTION: symbolic multiple-choice riddle in the style of the Ancient greek sphinx.
    A) option A
    B) option B
    C) option C
    D) option D
    CORRECT: A, B, C, or D only (This is hidden system data and must not be shown to the player)

    Requirements:
    - Keep content suitable for all ages.
    - No hate speech.
    - No discrimination.
    - No sexual content.
    - No self-harm content.
    - No illegal activities.
    """
    response = call_gpt(prompt)
# safety check
    if not response or response.strip() == "":
        return fallback_riddle()
    return response

#Read the AI's response and find the correct answer letter.
def get_correct(text):
    for line in text.split("\n"):
        line = line.strip().upper()

        if line.startswith("CORRECT"):
            parts = line.split(":")
            if len(parts) > 1:
                return parts[1].strip()

    return "A"  # default safe answer

# LIVE TIMER
def timed_input(prompt, limit=30):
    print(f"\n⏳ You have {limit} seconds to respond...")
    print("⚖️ The Sphinx is watching your speed...\n")

    start = time.time()
    answer = input(prompt).strip().upper()
    elapsed = time.time() - start

    print(f"\n⏱️ Time used: {round(elapsed, 2)}s")

    if elapsed > limit:
        print("⛔ TOO SLOW — YOU ARE ERASED")
        return None

    return answer

def reflection(): #Analyzes player based on their answers.
    prompt = f"""
You are the generative AI engine for "The Sphinx of Echoes," a psychological, atmospheric text-based console game.

Analyze this player's behavior based on their answers:
{player_state['answers']}

Return EXACT format:

STYLE: one word only (Logical, Emotional, Chaotic, Analytical)
REFLECTION: one short cryptic sentence
"""

    result = call_gpt(prompt)

    if not result or result.strip() == "": # Safetycheck, In case AI fails
        print("\n🪞 The Sphinx cannot interpret your mind.")
        return

    print("\n🪞 REFLECTION CHAMBER")
    print(result)

def ask_restart(): #only handles the user choice. Returns True if restarting, False if exiting
    choice = input("\n🔁 Restart the labyrinth? (Y/N): ").strip().upper()
    if choice == "Y":
        return True
    else:
        print("\n💀 The Sphinx remembers your failure.")
        return False


def end_game(reason):
    divider()
    type_text("FINAL JUDGMENT\n")

    print(f"Score: {player_state['score']}/5")

    if player_state["score"] >= 4:
        type_text("YOU UNDERSTOOD THE SPHINX")
    elif player_state["score"] >= 2:
        type_text("YOU WERE CLOSE TO TRUTH")
    else:
        type_text("YOU WERE LOST IN THE VOID")

    reflection()
    input("\nPress ENTER to continue...")

    return ask_restart()

def play():
    divider()
    type_text("ENTERING THE LABYRINTH...\n")

    for room in ROOM_SEQUENCE:
        divider()
        color = ROOM_COLORS.get(room["name"], BRIGHT_WHITE)

        print(color + f"⚡ {room['name'].upper()} ⚡" + RESET)

        content = generate_room_content(room["name"], room["Theme"])

        correct = get_correct(content)
        # REMOVE correct line before showing player
        clean_content = "\n".join(
             line for line in content.split("\n")
             if not line.strip().startswith("CORRECT")
        )
        type_text(color + clean_content + RESET)

        #TIME FAILURE
        answer = timed_input("\nYour answer (A/B/C/D): ")
        if answer is None:
            type_text(FAIL_COLOR + "\n⛔ TIME HAS COLLAPSED — YOU ARE ERASED" + RESET)
            return end_game("TIME FAILURE")

        
 
        answer = answer.strip().upper()

        #Invalid Input 

        if answer not in ["A", "B", "C", "D"]:
           type_text("\n🔴 INVALID THOUGHT — YOU ARE ERASED")
           return end_game("LOGIC FAILURE")
                

        player_state["answers"].append({
            "room": room["name"],
            "answer": answer,
            "correct": correct
        })

        #WRONG ANSWER
        if answer != correct:
            type_text(FAIL_COLOR + "\n🔴 WRONG ANSWER — YOU ARE ERASED" + RESET)
            return end_game("WRONG ANSWER")

        #SUCCESS
        player_state["score"] += 1
        type_text(SUCCESS_COLOR + "\n🟢 PASS — The Sphinx acknowledges you" + RESET)
    # 🎯 GAME COMPLETED
    return end_game("FULL COMPLETION")

def end_game(reason):
    divider()
    type_text("FINAL JUDGMENT\n")

    print(f"Score: {player_state['score']}/5")

    if player_state["score"] >= 4:
        type_text("YOU UNDERSTOOD THE SPHINX")
    elif player_state["score"] >= 2:
        type_text("YOU WERE CLOSE TO TRUTH")
    else:
        type_text("YOU WERE LOST IN THE VOID")

    reflection()
    input("\nPress ENTER to continue...")

    return ask_restart()

def restart_game():
    player_state["score"] = 0
    player_state["answers"] = []
    print("\n🔁 The Sphinx rewinds reality...\n")
    time.sleep(1)


if __name__ == "__main__":
    while True:
        intro()
        start = show_menu()

        if start:
            wants_to_restart = play()

            if wants_to_restart:
                restart_game() 
                continue       # Loops back to the intro menu
            else:
                break          # Ends game
                
                