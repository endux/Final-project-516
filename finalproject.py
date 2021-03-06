'''
NOTES:
    1) I think it'd be awesome if we could scrape some web pages or online books to
    get a huge number of paragraphs, rather than manually entering them. Then it could
    be used as a real-life tool!
'''

''' Steps:
1. Have a collection of 10 paragraphs or so.
2. When the user comes to the UI, display one text randomly with 5 fill-in-the-blanks for prepositions.
(This may be sentence by sentence)
3. Once the user submits, we should show how many they got right.
Note: We can use a list of prepositions for now - we don't need to POS tag.
'''
import random, re, string, operator
from bottle import get, post, request, route, run, redirect, template
from math import ceil

# This is a list of the top 25 most common English prepositions according to englishclub.com. Currently not being used...
preplist = ["with", "at", "from", "of", "in", "to", "for",
            "on", "by", "about", "as", "into", "like", "through", "after",
            "over", "between", "against", "during", "without", "before", "under",
            "around", "among"]

paragraph1 = ''' Iowa State University of Science and Technology, generally referred to as Iowa State, 
             is a public flagship land-grant and space-grant research university located in
             Ames, Iowa, United States. It is the largest university in the state of Iowa
             and the 3rd largest university in the Big 12 athletic conference.
             Iowa State is classified as a Research University with very high research activity 
             by the Carnegie Foundation for the Advancement of Teaching. 
             Iowa State is also a member of the Association of American Universities (AAU),
             which consists of 62 leading research universities in North America '''
paragraph2 = '''In 1872, the first courses were given in domestic economy
             (home economics, family and consumer sciences) and were taught by Mary B. Welch,
             the president's wife. Iowa State became the first land grant university 
             in the nation to offer training in domestic economy for college credit. 
             Iowa State began holding classes on August 20.
             '''
paragraph3 = '''But on the edge of town, drills were driven out of his mind by something else.
             As he sat in the usual morning traffic jam, he couldn't help noticing that there seemed to be
             a lot of strangely dressed people about. People in cloaks. Mr. Dursley couldn't bear
             people who dressed in funny clothes -- the getups you saw on young people!'''
paragraph4 = '''Francis Macomber had, half an hour before, been carried to his tent from the edge 
                of the camp in triumph on the arms and shoulders of the cook, the personal boys, 
                the skinner and the porters. The gun-bearers had taken no part in the demonstration. 
                When the native boys put him down at the door of his tent, he had shaken all their hands, 
                received their congratulations, and then gone into the tent and sat on the bed until his wife came in. 
                She did not speak to him when she came in and he left the tent at once to wash his face 
                and hands in the portable wash basin outside and go over to the dining tent to sit in a 
                comfortable canvas chair in the breeze and the shade.
             '''
paragraph5 = ''' A handsome manor house grew out of the darkness at the end of the straight drive, 
                lights glinting in the diamond-paned downstairs windows. Somewhere in the dark garden 
                beyond the hedge a fountain was playing. Gravel crackled beneath their feat as Snape
                and Yaxley sped toward the front door, which swung inward at their approach, 
                though nobody had visibly opened it.
            '''
paragraph6 = ''' The hallway was large, dimly lit, and sumptuously decorated, with a magnificent carpet 
                covering most of the stone floor. The eyes of the pale-faced portraits on the walls followed
                Snape and Yaxley as they strode past. The two men halted at a heavy wooden door leading
                into the next room, hesitated for the space of a heartbeat, then Snape turned the bronze handle.
             '''
paragraph7 = ''' The drawing room was full of silent people, sitting at a long and ornate table. The room's
                usual furniture had been pushed carelessly up against the walls. Illumination came from a roaring
                fire beneat a handsome marble mantelpiece surmounted by a gilded mirror. Snape and Yaxley
                lingered for a moment on the threshold.
             '''
paragraph8 = ''' The speaker was seated directly in front of the fireplace, so that it was difficult, at first,
                for the new arrivals to make out more than his silhouette. As they drew nearer, however, his face
                shone through the gloom, hairless, snakelike, with slits for nostrils and gleaming red eyes whose
                pupils were vertical. He was so pale that he seemed to emit a pearly glow.
             '''
paragraph9 = ''' An LAS cross-disciplinary program, the Linguistics Program is housed in the Department of English. 
                The program offers a major and a minor for undergraduate students wanting to learn about theory and 
                practice in the study of language. Linguistics is the study of how human languages are structured 
                and used. This may involve discovering patterns for how words are created, how sounds are combined 
                to create meanings, how sentences are formed, and how speakers use language to communicate meaning. 
                Students explore topics including the sounds and grammar of language, languages of the world, 
                computational analysis of language, and language teaching.
             '''
coolparagraph = ''' Pella is a city in Marion County, Iowa, United States, with a population of 10,352 at the time 
                of the 2010 U.S. Census. Founded by immigrants from the Netherlands, it is forty miles southeast 
                of Des Moines. Pella is the home of Central College, as well as several manufacturing companies, 
                including Pella Corporation and Vermeer Manufacturing Company. In 1847, 800 Dutch immigrants led 
                by Dominee (Minister) Hendrik (Henry) P. Scholte settled the area known as Pella. The name "Pella" 
                is a reference to Perea, where the Christians of Jerusalem had found refuge during the Roman–Jewish 
                war of 70; the name was selected because the Dominee and the rest were also seeking religious freedom.
              '''
lameparagraph = ''' Knoxville is a city in Marion County, Iowa, United States. The population was 7,313 
                    at the 2010 census, a decrease from 7,731 in the 2000 census. It is the county seat of Marion County.
                    Knoxville is home of the National Sprint Car Hall of Fame & Museum, located next to the famous 
                    Knoxville Raceway dirt track. The site for the future county seat of Marion County was selected 
                    because it was within a mile of the geographic center of the county, reasonably level and near 
                    a good source of timber. The first town lots were sold in 1845, and the town was named after 
                    Knoxville, a small town in Iowa which was created in 1845 to be the county seat for Marion County.
                '''
paragraphs = [paragraph1, paragraph2, paragraph3, paragraph4, paragraph5, paragraph6, paragraph7, paragraph8, paragraph9, coolparagraph, lameparagraph]

def getParagraphAnswers(difficulty, paragraphChoice):
    global chosenBlanks, count
    numBlanks = 0
    paragraphwordlist = paragraphChoice.split()
    # print("paragraphwordlist",paragraphwordlist,"\n")
    paragraphpreplist = []
    index = -1
    for word in paragraphwordlist:
        index += 1
        if word in preplist:
            tmp = [index,word]
            paragraphpreplist.append(tmp)
    # print("paragraphpreplist",paragraphpreplist,"\n")
    if difficulty == 'Easy':
        numBlanks = ceil(int(len(paragraphpreplist))*0.5)
    if difficulty == 'Intermediate':
        numBlanks = ceil(int(len(paragraphpreplist)) * 0.75)
    if difficulty == 'Difficult':
        numBlanks = len(paragraphpreplist)
    random.shuffle(paragraphpreplist)
    chosenBlanks = paragraphpreplist[:numBlanks]
    chosenBlanks = sorted(chosenBlanks, key=operator.itemgetter(0))
    # print("chosenblanks",chosenBlanks,"\n")
    count = 1
    for item in chosenBlanks:
        paragraphwordlist[item[0]] = '<input name="answer' + str(count) + '" type="text" autocomplete="off"/>'
        count += 1
    newParagraph = " ".join(paragraphwordlist)
    # print("newParagraph",newParagraph,"\n")
    return(newParagraph,numBlanks)


HEADER = ''' <html>   
        </hmtl>
         '''

@route('/')
@get('/login')
def loginPage():
    return '''
    <center>
    <head>
    <body bgcolor="#f5f5f0">
    <title>Practicing Prepositions</title>
    <h1> <font color="#c00"> Welcome to Preposition Practice! </h1> 
    <img src="http://proacademy.in/blog/wp-content/uploads/2017/12/prepositions.png" width="250"
     height="170.5"> </img>
    </head>
    <form action="/login" method="post">
        <h3> <font color="#c00"> Enter your name below to begin. </h3>
        <font color="black"> Name: <input name="name" type="text" /><br>
        <input value="Submit" type="submit" />
        <select name="difficulty">
           <option value="Easy">Easy</option>
           <option value="Intermediate">Intermediate</option>
           <option value="Difficult">Difficult</option>
        </select>
    </form>
    </center>
    '''

@post('/login')

@route('/collect_answers')
def collect_answers():
    global paragraphs, paragraphChoice
    paragraphChoice = random.choice(paragraphs)
    # print(paragraphChoice, "I've been reassigned")
    difficulty = request.forms.get('difficulty')
    newParagraph = getParagraphAnswers(difficulty,paragraphChoice)[0]

    '''To collect the user's answers.
    Inputs: The paragraph and its answers.
    Outputs: The updated replaced paragraph, the index of each answer.'''
    return template('collect_answers.tpl', newParagraph=newParagraph)

@post('/feedbackpage')
def feedbackpage():
    userscore = 0
    global paragraphChoice, count, chosenBlanks
    counter = 1
    data = {}
    for i in range(count-1):
        answer = "answer"+str(counter)
        data[answer] = request.forms.get(answer)
        counter += 1
    # print(data)
    answers = data.values()
    # print("answers",answers)
    for i in chosenBlanks:
        for j in answers:
            if i[1] == j:
                userscore += 1
                continue
    # print(userscore)
    return template('feedbacktemplate.tpl', userscore=userscore, paragraphChoice=paragraphChoice, data=data, count=count)

@post('/redirectpage')
def redirectpage():
    redirect('/collect_answers')

run(reloader=True)



# # useranswer1 = request.forms.get('answer1')
# # print(useranswer1, "is it empty?")
# useranswer2 = request.forms.get('answer2')
# useranswer3 = request.forms.get('answer3')
# useranswer4 = request.forms.get('answer4')
# useranswer5 = request.forms.get('answer5')
# if useranswer1 == answers[0]:
#     userscore +=1
# if useranswer2 == answers[1]:
#     userscore +=1
# if useranswer3 == answers[2]:
#     userscore+=1
# if useranswer4 == answers[3]:
#     userscore+=1
# if useranswer5 == answers[4]:
#     userscore+=1










# Blank 1: <input name="answer1" type="text" autocomplete="off"/><br>
#     Blank 2: <input name="answer2" type="text" autocomplete="off"/><br>
#     Blank 3: <input name="answer3" type="text" autocomplete="off"/><br>
#     Blank 4: <input name="answer4" type="text" autocomplete="off"/><br>
#     Blank 5: <input name="answer5" type="text" autocomplete="off"/><br>





#Beginning the actual programming:
'''
def getRandomParagraph():
    paragraphOptions = [paragraph1, paragraph2, paragraph3]
    global paragraphChoice
    paragraphChoice = random.choice(paragraphOptions)
    global answers
    if paragraphChoice == paragraph1:
        answers = paragraph1answers
    elif paragraphChoice == paragraph2:
        answers = paragraph2answers
    elif paragraphChoice == paragraph3:
        answers = paragraph3answers
    return paragraphChoice, answers
'''