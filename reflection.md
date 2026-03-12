# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
When I first ran it, it actually displayed an error regarding an architecture mismatch for numpy. I used AI to help resolve it by reinstalling numpy. After it was resolved, I was able to enter a guess on the game.
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
The hints were reversed; it would say "Go higher" although it should say "Go lower." Also, the attempts weren't counted correctly, so it said "Out of attempts" when I still had one attempt left. When I clicked "New Game," it wouldn't let me submit any more guesses because the app seemed stuck in the "game over" state.
---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used Copilot in VSCode.
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
 For the bug about the number of attempts, the initial value of st.session_state.attempts was 1. The AI fixed it to 0 and I verified the result by running the game again and the behavior was expected.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
I told the AI to create pytest cases to target the bugs fixed. It created tests and all of them passed, but it was misleading because after I moved the check_guess() function to logic_utils.py, 3 of the pre-existing tests were calling the real function (no longer NotImplementedError), but their assertions compare the full tuple to just a string.
---
 
## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I tested the behavior manually on the app by using a variety of inputs, and adding tests to ensure that each function worked.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
I ran `python3 -m pytest -q` after moving the functions into `logic_utils.py` and adding new test coverage. One useful test checked that when the guess is too high, the hint contains "LOWER" and not "HIGHER," which confirmed the swapped hint bug was fixed. I also added parsing and scoring tests to verify edge cases like empty input, float-like strings, and win scoring minimums. The full suite passed with 28 tests, which gave me confidence the fixes worked together.
- Did AI help you design or understand any tests? How?
Yes, AI helped propose regression tests for the exact bugs I fixed, especially hint direction and off-by-one attempt counting. It also helped me broaden coverage using parameterized tests so I could test several inputs quickly. One important lesson was that passing tests are only meaningful if assertions match the actual return type, so I updated assertions to check the `outcome` from `(outcome, message)` tuples.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
The secret number kept changing because Streamlit reruns the script on every interaction, and values can reset if they are not stored correctly in `st.session_state`. If the secret is generated each rerun instead of only once, the target moves between guesses. That made the game feel inconsistent and impossible to debug.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
I would explain that Streamlit reruns your script top to bottom every time the user clicks a button or changes an input. `st.session_state` is like persistent memory that survives those reruns for that user session. If you put important game values there, your app behaves like a real stateful game instead of resetting every interaction.
- What change did you make that finally gave the game a stable secret number?
I made sure the secret is only initialized when `"secret"` is not already in `st.session_state`, instead of regenerating it on each rerun. I also kept reset behavior explicit by only assigning a new secret during "New Game." That made the secret stable during a round and change only when intended.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
I want to keep the habit of writing regression tests immediately after fixing a bug so it cannot quietly return later. I also liked moving logic into utility functions because it made tests cleaner and faster to run. In future projects, I will keep using small, focused prompts for AI (one bug at a time) and verify each change with tests.
- What is one thing you would do differently next time you work with AI on a coding task?
Next time, I would validate function signatures and return shapes earlier before trusting test results. I would also ask AI to include why each assertion matters so I can quickly spot weak or misleading tests. That would reduce time spent fixing tests that pass for the wrong reason.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
This project showed me that AI can accelerate debugging and test creation, but I still need to review logic and assertions carefully. I now treat AI output as an assistant to help debug but not a final product.
