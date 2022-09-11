from startGame import StartGame
from login import Login

email = '*******'
password = '******'
color = 'black/white/random'
timPerMove = "0.5" #0.5 is half a secend 
modus = 'playAi/playFriend/ranked'

#Login().login(email, password, color, timPerMove, modus)
StartGame().playAI(color="white", timePerMove=0.5)