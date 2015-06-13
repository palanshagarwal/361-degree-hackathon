from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import JsonResponse

b=None
ai=None

def ping(request):
    data={"ok":True}
    return JsonResponse(data)

class Board():
    def __init__(self,n,pehleAI):
        self.board = [[0 for x in xrange(n)] for x in xrange(n)] #declare board of size n
        if pehleAI:
            self.board[0][0]=1
            self.board[n-1][n-1]=2
        else:
            self.board[0][0]=2
            self.board[n-1][n-1]=1
        self.size=n
        self.pehleAI=pehleAI

    def retPehleAI(self):
        return self.pehleAI


    def isLegalMove(self,row,column):
        if row>=self.size or column>=self.size or column<0 or row<0:
            return False 
        elif self.board[row][column]==0:
            return True
        return False

    def placeMove(self,row,column,player):
        if not self.isLegalMove(row,column):
            print 'Illegal move'
        else:
            self.board[row][column]=int(player)

    def undoMove(self,row,column):
        self.board[row][column]=0

    def displayBoard(self):
        for _ in xrange(len(self.board)):
            print self.board[_]


# x = Board(8)
# print x.board
# print x.size
# print x.isLegalMove(1,2)
# x.placeMove(9,9,1)
# print x.isLegalMove(2,3)
# print x.undoMove(0,1)
# print x.isLegalMove(1,2)
# x.displayBoard()

class Chess():
    aiPosX = 0
    aiPosY = 0
    aiPosXtt = 0
    aiPosYtt = 0
    nextMoveLocationY = -1
    nextMoveLocationX = -1
    maxDepth = 3
    hPosX = 0
    hPosY = 0
    hPosXtt = 0
    hPosYtt = 0

    def __init__(self,b):
        self.game=b
        self.size = len(b.board)

    def letOpponentMove(self,m):
        #move_inp = raw_input("Your move:")
        move = m.split('|')
        self.game.placeMove(int(move[0])-1,int(move[1])-1,2)
        self.hPosX=int(move[0])-1
        self.hPosY=int(move[1])-1

    def calculateScore(self,aiScore):
        return 5**aiScore

    def evaluateBoard(self,b):
        score=0
        blanks = 0
      
        for i in xrange(self.aiPosXtt-1,self.aiPosXtt+2):
            for j in xrange(self.aiPosYtt-1,self.aiPosYtt+2):
                if i==self.hPosXtt and j==self.hPosYtt:
                    score = (-10**5)
                    i = 25
                    break
                elif b.board[i][j]==0:
                    blanks+=1

        if i!=25:
            score=self.calculateScore(blanks)
        return score


    def minimax(self,depth, turn, alpha, beta):
       
        if int(beta)<=int(alpha):
            if int(turn) == 1:
                return 10**9
            else:
                return -10**9
       
        if int(depth) == int(self.maxDepth):
          return self.evaluateBoard(self.game)
       
        maxScore=-10**9
        minScore = 10**9

        for i in xrange(self.aiPosX-1,self.aiPosX+2):
            for j in xrange(self.aiPosY-1,self.aiPosY+2):
                currentScore = 0
                if i==self.hPosX and j==self.hPosY:
                    self.nextMoveLocationY = j
                    self.nextMoveLocationX = i  
                    return 0

                if not self.game.isLegalMove(i,j):
                    continue

                if int(turn)==1:
                    self.game.placeMove(i,j,1);
                    currentScore = self.minimax(depth+1, 2, alpha, beta)
                   
                    if depth==0:
                        print(currentScore, maxScore)
                        if currentScore >= maxScore:
                            self.nextMoveLocationY = j
                            self.nextMoveLocationX = i      

                        maxScore = max(currentScore, maxScore)
                        alpha = max(currentScore, alpha)

                elif int(turn)==2:
                    self.game.placeMove(i,j,2)
                    currentScore = self.minimax(depth+1, 1, alpha, beta)
                    minScore = min(currentScore, minScore)
                    beta = min(currentScore, beta)
                self.game.undoMove(i,j)
        if turn==1:
            return maxScore
        else:
            return minScore

    def playAgainstAIConsole(self):
        # if self.game.retPehleAI(): 
        #     aiPosX =1; aiPosY=1
        #     self.game.placeMove(1,1,1)
        # else: 
        #     self.letOpponentMove()
        #     self.game.placeMove(self.size-2,self.size-2,1)
        #     self.aiPosY = self.size-2
        #     self.aiPosX = self.size-2
        
        # while True: 
            
            # self.letOpponentMove()
        self.minimax(0, 1, -10**9, 10**9)
        temp = (self.nextMoveLocationX,self.nextMoveLocationY)
        print "temp is" 
        print(temp)
        self.game.placeMove(temp[0],temp[1], 1)
        self.aiPosX = temp[0]
        self.aiPosY=temp[1]

        return str(temp[0]+1) +'|' + str(temp[1]+1)
            # print self.game.displayBoard()
            
def main(n,pehl):
    global b
    global ai
    b = Board(n,pehl)
    ai = Chess(b)
    # ai.playAgainstAIConsole()


def start(request):
    peh = request.GET.get('y', '')
    if peh=='1|1':
        pehl=True
    else:
        pehl=False
    n = request.GET.get('g', '')
    main(int(n),pehl)
    data={"ok":True}
    return JsonResponse(data)


def play(request):
    move = request.GET.get('m', '')
    ai.letOpponentMove(move)
    P=ai.playAgainstAIConsole()
    data={"m":P}
    return JsonResponse(data)

