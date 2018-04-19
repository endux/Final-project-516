<center>
<autocomplete="off">
<h3> <font color="black">How did you do?</h3>
<form action="/redirectpage" method="post">
    <font color="blue">Your score: {{userscore}} out of {{count}} <br><br>
    <font color="black">{{paragraphChoice}} <br><br>
    <font color="blue">Here are your answers: {{' '.join(answers)}} <br>
    <font color="blue">Here are the correct answers: {{chosenBlanks}} <br>
    <font color="black"><input value="Practice again!" type="submit" />
</form>
</center>
