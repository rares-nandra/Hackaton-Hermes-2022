var PageSwiper;
var Navbar;
var ActiveMenuSlider;
var ActiveMenuSliderBaseDelay;

var RightKeyPressed = false;
var LeftKeyPressed = false;

let ugly = 150

window.addEventListener("load", function() 
{
	/* Initializes the Page Swiper */

	PageSwiper = new Swiper("#PagesContainer", {});
	ActiveMenuSlider = document.getElementById("ActiveMenu");

	PageSwiper.on("slideChange", function () 
	{
		HandlePageChange();
	});

	/* Initializes the navbar */

	Navbar = document.getElementsByTagName("nav")[0];

	Navbar.style = "transition: bottom ease 0.85s;"
		Navbar.style.bottom = "6vh";

	ActiveMenuSlider.style.marginLeft = String(9.33 + 33.33333 * PageSwiper.activeIndex) + "%";

	/* Initializes the Shortcuts */

	document.onkeydown = function(Event)
	{
		Event = Event || window.event;

		if((Event.key == "ArrowRight" || Event.key == "Right") && (RightKeyPressed == false)) 
		{
			SlideToPage(PageSwiper.activeIndex + 1);
			RightKeyPressed = true;
		}
		else if((Event.key == "ArrowLeft" || Event.key == "Left") && (LeftKeyPressed == false)) 
		{
			SlideToPage(PageSwiper.activeIndex - 1);
			LeftKeyPressed = true;
		}
	}

	this.document.onkeyup = function(Event)
	{
		if(Event.key == "ArrowRight" || Event.key == "Right") 
		{
			RightKeyPressed = false;
		}
		else if(Event.key == "ArrowLeft" || Event.key == "Left") 
		{
			LeftKeyPressed = false;
		}
	}

    diseases = document.getElementsByClassName("diseases_container");

    for(let i = 0; i < diseases.length; i++)
    {
        if(String(diseases[i].innerHTML).includes("Blindness"))
        {
            Blind = true;
        }
    }

    if(document.getElementById("favs-container").innerHTML === "")
    {
        document.getElementById("favs-container").innerHTML = "<h1 class = 'text-center'>No favorites yet !</h1>";
    }
});

/* Page Swiper */

function HandlePageChange()
{
	ActiveMenuSlider.style.marginLeft = String(9.33 + 33.33333 * PageSwiper.activeIndex) + "%";
}

function SlideToPage(PageIndex)
{
	var SlideDelta = Math.abs(PageSwiper.activeIndex - PageIndex);

	ActiveMenuSlider.style.transitionDuration = String((300 * SlideDelta) / 1000) + "s";
	PageSwiper.slideTo(PageIndex, 300 * SlideDelta, true);
	setTimeout(ResetMenuDelay, 300 * SlideDelta);

}

function ResetMenuDelay()
{
	ActiveMenuSlider.style.transitionDuration = "0.3s";
}

const elements = document.querySelectorAll(['range-slider']);



const allRanges = document.querySelectorAll(".range-wrap");
allRanges.forEach(wrap => 
{
    const range = wrap.querySelector(".range");
    const bubble = wrap.querySelector(".bubble");

    range.addEventListener("input", () => 
    {
        setBubble(range, bubble);
    });
    
    setBubble(range, bubble);
});

function setBubble(range, bubble) 
{
    let val = range.value;

    if(val < 5)
    {
        val = 5;
    }

    val = val * 3;
    newVal = val / 3;
    
    ugly = val;
    bubble.innerHTML = val + " km";
    bubble.style.left = `calc(${newVal}% + (${0 - newVal * 0.15}px))`;
}

function search()
{
    let destinationType = document.getElementById("vacation-type-selector").options[document.getElementById("vacation-type-selector").selectedIndex].text;
    // destinationType = destinationType.toLowerCase().replace(" ", "");

	if(destinationType==="Mountain"){
		destinationType="geological_formations"
	} else if(destinationType==="Seaside") {
		destinationType="beaches"
	} else {
		destinationType="urban_environment"
	}

    let covid = document.getElementById("covid-toggle").checked;
    let distance = ugly;

    data = {
        "vacation-type": destinationType,
        "covid": covid,
        "distance": distance
    }

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/search', true);
    xhr.setRequestHeader('Content-type', 'application/json');

    
    document.getElementById("feed").innerHTML = "";
    document.getElementById("loader").style.visibility = "unset";

    xhr.onload = function () 
    {
        console.log(this.responseText);
        document.getElementById("loader").style.visibility = "hidden";
        renderDestinations(JSON.parse(this.responseText));
    };
    
    xhr.send(JSON.stringify(data));
}

function renderDestinations(dest)
{
    for(let i = 0; i < dest.length; i++)
    {
        if(i % 2)
        {
            a = false;
        }
        else
        {
            a = true;
        }
        renderDestination(dest[i], a);
    }
}

function renderDestination(destination, left)
{
    console.log(destination);

    let BlindGuides = "";

    if(typeof Blind !== 'undefined')
    {
        BlindGuides = "<p class = 'FeedText' style = 'margin-top: -75px'>Marcel - Local guide for blind people 45$</p><p style = 'margin-top: -75px' class = 'FeedText'>George - Local guide for blind people 50$</p>";
    }

    let feed = document.getElementById("feed");

    if(left)
    {
        ImageOrientation = "FeedImageRight";
        TextOrientation = "FeedTextRight";
    }
    else
    {
        ImageOrientation = "FeedImageLeft";
        TextOrientation = "FeedTextLeft";
    }

    let ImageLink = destination["image_url"];
    let Name = destination["name"];
    let HospitalName = destination["hospital"];
    let HospitalDistance = destination["hospital_distance"];

    destinationHTML = `
        <div class = "row">
            <div class = "FeedPost">
                <div class = "BackgroundImage FeedImage ` + ImageOrientation + `" style = "background-image: url(` + ImageLink + `);"></div>

                <div class = "FeedTextContainer ` + TextOrientation + ` text-center">
                    <h1 class = "FeedTitle" id = "FeedElement">` + Name + `</h1>
                    <p class = "FeedText">The closest hospital's name is ` + HospitalName + ` at a distance of ` + String(HospitalDistance) + ` kilometers</p>                        
                    
                    ` + BlindGuides + `                      
                    <button type = "button" class="big gradient-border animation-increase" id="favorite-submit" onclick = "addFavorite(this)">Toggle favorite</button>
                </div>
            </div>
        </div>
    `;

    feed.innerHTML = feed.innerHTML + destinationHTML;
}

function addFavorite(elem)
{
    html_to_send = "<div class = 'row'>" + elem.parentElement.parentElement.parentElement.innerHTML + "</div>";

    data = {
        "html": String(html_to_send)
    }

    var xhr = new XMLHttpRequest();
    xhr.open('POST', '/favorite', true);
    xhr.setRequestHeader('Content-type', 'application/json');

    xhr.onload = function () 
    {
        console.log(this.responseText);
    };
    
    xhr.send(JSON.stringify(data));
}