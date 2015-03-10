// this function adds a new email input to our form
function addWord()
{
	wordcounter++;
	document.getElementById('wordcontainer').innerHTML+='<div>Word '+wordcounter+': <input type="text" name="word"><br></div>';
}