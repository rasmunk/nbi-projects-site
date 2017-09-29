/**
 * Created by rasmusmunk on 27/09/2017.
 */

function createProjectTile(project) {
    var newHeader = document.createElement('h3');
    newHeader.className = "card-title";
    newHeader.innerText = project.name;

    var newBody = document.createElement('p');
    newBody.className = "card-text";
    newBody.innerText = project.description;

    var newCaption = document.createElement('div');
    newCaption.className = "caption";
    newCaption.appendChild(newHeader);
    newCaption.appendChild(newBody);

    var newImage = document.createElement('img');
    newImage.src = "/images/" + project.image;
    newImage.alt = "Project";

    var newThumb = document.createElement('div');
    newThumb.className = "thumbnail mb-4";
    newThumb.appendChild(newImage);
    newThumb.appendChild(newCaption);

    var newLink = document.createElement('a');
    newLink.className = "d-block mb-4";
    newLink.href = "/show/" + project._id;
    newLink.appendChild(newThumb);

    var newDiv = document.createElement('div');
    newDiv.className = "col-sm-6 col-md-4 col-lg-3";
    newDiv.appendChild(newLink);
    return newDiv;
}


$(document).ready(function() {
   setupTagSearch(createProjectTile);
});