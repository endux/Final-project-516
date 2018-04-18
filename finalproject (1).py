''' Steps:
1. Have a collection of 10 paragraphs or so.
2. When the user comes to the UI, display one text randomly with 5 fill-in-the-blanks for prepositions.
(This may be sentence by sentence)
3. Once the user submits, we should show how many they got right.
Note: We can use a list of prepositions for now - we don't need to POS tag.
'''
#Pre-Processing:
import random, re, string
from bottle import get, post, request, route, run, redirect, template

''' This is a list of the top 25 most common English prepositions according to englishclub.com. Currently not being used...
preplist = ["with", "at", "from", "of", "in", "to", "for",
            "on", "by", "about", "as", "into", "like", "through", "after",
            "over", "between", "against", "during", "without", "before", "under",
            "around", "among"] '''

paragraph1 = ''' Iowa State University of Science and Technology, generally referred to as Iowa State, 
             is a public flagship land-grant and space-grant research university located ___1___
             Ames, Iowa, United States. It is the largest university in the state ___2___ Iowa
             and the 3rd largest university ___3___ the Big 12 athletic conference.
             Iowa State is classified ___4___ a Research University with very high research activity 
             by the Carnegie Foundation for the Advancement of Teaching. 
             Iowa State is also a member of the Association of American Universities (AAU),
             which consists ___5___ 62 leading research universities in North America '''

paragraph1answers = ["in", "of", "in", "as", "of"]

paragraph2 = '''___1___ 1872, the first courses were given in domestic economy
             (home economics, family and consumer sciences) and were taught ___2___ Mary B. Welch,
             the president's wife. Iowa State became the first land grant university 
             ___3___ the nation to offer training in domestic economy ___4___ college credit. 
             Iowa State began holding classes ___5___ August 20.
             '''
paragraph2answers = ["in", "by", "in", "for", "on"]

paragraph3 = '''But ___1___ the edge ___2___ town, drills were driven out of his mind by something else.
             As he sat ___3___ the usual morning traffic jam, he couldn't help noticing that there seemed to be
             a lot of strangely dressed people about. People in cloaks. Mr. Dursley couldn't bear
             people who dressed ___4___ funny clothes -- the getups you saw ___5___ young people!'''
paragraph3answers = ["on", "of", "in", "in", "on"]

paragraph4 = '''Francis Macomber had, half an hour before, been carried ___1___ his tent ___2___ the edge 
                ___3___ the camp in triumph on the arms and shoulders of the cook, the personal boys, 
                the skinner and the porters. The gun-bearers had taken no part ___4___ the demonstration. 
                When the native boys put him down at the door of his tent, he had shaken all their hands, 
                received their congratulations, and then gone ___5___ the tent and sat on the bed until his wife came in. 
                She did not speak to him when she came in and he left the tent at once to wash his face 
                and hands in the portable wash basin outside and go over to the dining tent to sit in a 
                comfortable canvas chair in the breeze and the shade.
             '''
paragraph4answers = ["to", "from", "of", "in", "into"]

paragraph5 = ''' A handsome manor house grew out ___1___ the darkness ___2___ the end ___3___ the straight drive, 
                lights glinting ___4___ the diamond-paned downstairs windows. Somewhere ___5___ the dark garden 
                beyond the hedge a fountain was playing. Gravel crackled beneath their feat as Snape
                and Yaxley sped toward the front door, which swung inward at their approach, 
                though nobody had visibly opened it.
            '''
paragraph5answers = ["of", "at", "of", "in", "in"]

paragraph6 = ''' The hallway was large, dimly lit, and sumptuously decorated, ___1___ a magnificent carpet 
                covering most ___2___ the stone floor. The eyes of the pale-faced portraits ___3___ the walls followed
                Snape and Yaxley as they strode past. The two men halted at a heavy wooden door leading
                ___4___ the next room, hesitated ___5___ the space of a heartbeat, then Snape turned the bronze handle.
             '''
paragraph6answers = ["with", "of", "on", "into", "for"]

paragraph7 = ''' The drawing room was full ___1___ silent people, sitting ___2___ a long and ornate table. The room's
                usual furniture had been pushed carelessly up against the walls. Illumination came ___3___ a roaring
                fire beneath a handsome marble mantelpiece surmounted ___4___ a gilded mirror. Snape and Yaxley
                lingered ___5___ a moment on the threshold.
             '''
paragraph7answers = ["of", "at", "from", "by", "for"]

paragraph8 = ''' An LAS cross-disciplinary program, the Linguistics Program is housed ___1___ the Department of English. 
                The program offers a major and a minor ___2___ undergraduate students wanting to learn ___3___ theory and 
                practice in the study of language. Linguistics is the study ___4___ how human languages are structured 
                and used. This may involve discovering patterns for how words are created, how sounds are combined 
                to create meanings, how sentences are formed, and how speakers use language to communicate meaning. 
                Students explore topics including the sounds and grammar ___5___ language, languages of the world, 
                computational analysis of language, and language teaching.
             '''
paragraph8answers = ["in", "for", "about", "of", "of"]

coolparagraph = ''' Pella is a city ___1___ Marion County, Iowa, United States, ___2___ a population of 10,352 ___3___ the time 
                of the 2010 U.S. Census. Founded ___4___ immigrants from the Netherlands, it is forty miles southeast 
                of Des Moines. Pella is the home ___5___ Central College, as well as several manufacturing companies, 
                including Pella Corporation and Vermeer Manufacturing Company. In 1847, 800 Dutch immigrants led 
                by Dominee (Minister) Hendrik (Henry) P. Scholte settled the area known as Pella. The name "Pella" 
                is a reference to Perea, where the Christians of Jerusalem had found refuge during the Roman–Jewish 
                war of 70; the name was selected because the Dominee and the rest were also seeking religious freedom.
              '''
coolparagraphanswers = ["in", "with", "at", "by", "of"]

lameparagraph = ''' Knoxville is a city in Marion County, Iowa, United States. The population was 7,313 
                    at the 2010 census, a decrease ___1___ 7,731 in the 2000 census. It is the county seat ___2___ Marion County.
                    Knoxville is home of the National Sprint Car Hall of Fame & Museum, located next to the famous 
                    Knoxville Raceway dirt track. The site ___3___ the future county seat of Marion County was selected 
                    because it was within a mile of the geographic center of the county, reasonably level and near 
                    a good source of timber. The first town lots were sold ___4___ 1845, and the town was named after 
                    Knoxville, a small town in Iowa which was created in 1845 to be the county seat ___5___ Marion County.
                '''
lameparagraphanswers = ["from", "of", "for", "in", "for"]

#need to figure out how to do this...?
HEADER = ''' <html>   
        </hmtl>
         '''

#Beginning the actual programming:

def getRandomParagraph():
    paragraphOptions = [paragraph1, paragraph2, paragraph3, paragraph4, paragraph5, paragraph6, paragraph7, paragraph8, coolparagraph, lameparagraph]
    global paragraphChoice
    paragraphChoice = random.choice(paragraphOptions)
    global answers
    if paragraphChoice == paragraph1:
        answers = paragraph1answers
    elif paragraphChoice == paragraph2:
        answers = paragraph2answers
    elif paragraphChoice == paragraph3:
        answers = paragraph3answers
    elif paragraphChoice == paragraph4:
        answers = paragraph4answers
    elif paragraphChoice == paragraph5:
        answers = paragraph5answers
    elif paragraphChoice == paragraph6:
        answers = paragraph6answers
    elif paragraphChoice == paragraph7:
        answers = paragraph7answers
    elif paragraphChoice == paragraph8:
        answers = paragraph8answers
    elif paragraphChoice == coolparagraph:
        answers = coolparagraphanswers
    elif paragraphChoice == lameparagraph:
        answers = lameparagraphanswers
    return paragraphChoice, answers

#"logging them in" just for fun...
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
        <font color="black"> Name: <input name="name" type="text" autocomplete="off"/><br>
        <input value="Submit" type="submit" />
    </form>
    </center>
    '''

@post('/login')

@route('/collect_answers')
def collect_answers():
    '''To collect the user's answers.
    Inputs: The paragraph and its answers.
    Outputs: The updated replaced paragraph, the index of each answer.'''
    getRandomParagraph()
    return template('collect_answers.tpl', paragraphChoice=paragraphChoice)

@post('/feedbackpage')
def feedbackpage():
    userscore = 0
    useranswer1 = request.forms.get('answer1')
    useranswer2 = request.forms.get('answer2')
    useranswer3 = request.forms.get('answer3')
    useranswer4 = request.forms.get('answer4')
    useranswer5 = request.forms.get('answer5')
    if useranswer1.casefold() == answers[0]:
        userscore +=1
    if useranswer2.casefold() == answers[1]:
        userscore +=1
    if useranswer3.casefold() == answers[2]:
        userscore+=1
    if useranswer4.casefold() == answers[3]:
        userscore+=1
    if useranswer5.casefold() == answers[4]:
        userscore+=1
    return template('feedbacktemplate.tpl', userscore=userscore, paragraphChoice=paragraphChoice,
                    answers=answers, useranswer1=useranswer1, useranswer2=useranswer2, useranswer3=useranswer3,
                    useranswer4=useranswer4, useranswer5=useranswer5)

@post('/redirectpage')
def redirectpage():
    redirect('/collect_answers')

run()
