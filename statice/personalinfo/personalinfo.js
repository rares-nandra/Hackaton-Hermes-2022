window.onload = function() 
{
    let checkboxes = document.getElementsByClassName("teIubDani");

    for(let i = 0; i < checkboxes.length; i++)
    {
        setDisease(checkboxes[i]);
    }
};


function setDisease(elem)
{
    if(elem.checked)
    {
        elem.value = "1";
    }
    else
    {
        elem.value = "0";
    }
}