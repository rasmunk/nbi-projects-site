/**
 * Created by rasmusmunk on 27/09/2017.
 */
/*jshint esversion: 6 */
"use strict";

function setupAreaSelection() {
    console.log("Called");
    let active_buttons = $()
    let selection = $('.btn-projects');


    selection.on('click', function () {
        window.location.href = '/projects/1';
        // console.log("Activated");
        // $.ajax({
        //     url: '/projects/1',
        //     type: 'GET',
        //     success: function (response) {
        //         let gridItems = document.getElementById('grid-items');
        //         removeChildren(gridItems);
        //         for (let results in response) {
        //             if (response.hasOwnProperty(results)) {
        //                 for (let result in response[results]) {
        //                     if (response[results].hasOwnProperty(result)) {
        //                         let tile = createProjectTile(response[results][result]);
        //                         // Access thumbnail child element -> attach hover effect
        //                         setupThumbnailHoverEffect(tile.getElementsByClassName('thumbnail')[0]);
        //                         gridItems.appendChild(tile);
        //                     }
        //                 }
        //             }
        //         }
        //     },
        //     error: function (error) {
        //         console.log(error);
        //     }
    });
}

$(document).ready(function () {
    setupAreaSelection();
});