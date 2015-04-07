// this function adds a new email input to our form
var wordcounter = 0;
function addWord()
{
	wordcounter++;
	if (wordcounter == 1)
	{
		document.getElementById('wordcontainer').innerHTML+='<button style="color: black !important;" type="button" id="rbutton" onclick="removeWord()">Remove Word</button><p>Word '+wordcounter+': <input style="color: black !important;" type="text" name="word"><br></p>';
	}
	else
	{
		document.getElementById('wordcontainer').innerHTML+='<p>Word '+wordcounter+': <input style="color: black !important;" type="text" name="word"><br></p>';
	}
}
function removeWord()
{
	wordcounter--;
	listNodes = document.getElementsByTagName("p");
	parent = document.getElementById('wordcontainer');
	if (wordcounter == 0)
	{
		parent.removeChild(listNodes[wordcounter]);
		child = document.getElementById("rbutton");
		parent.removeChild(child);
	}
	else
	{
		parent.removeChild(listNodes[wordcounter])
	}
}
	