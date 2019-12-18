/**
 * Created by rasmusmunk on 27/09/2017.
 */
/*jshint esversion: 6 */
"use strict";


function setupAreaSelection() {
    let selection = $('.btn-projects');

    selection.on('click', function (e) {
        // Get the active area
        let data = {
            'csrf_token': $('#csrf_token').val()
        };
        if (!this.classList.contains('active')) {
            data.area = this.id;
        } else {
            // Stop bootstrap in its tracks
            e.stopImmediatePropagation();
            e.preventDefault();
            $('.btn-group label').removeClass('active');
        }

        $.ajax({
            url: '/projects',
            data: data,
            type: 'POST',
            success: function (response) {
                // populate projects to grid
                if (response.hasOwnProperty('data') &&
                    response.data.hasOwnProperty('projects')) {
                    populateGrid(response.data.projects);
                }
            },
            error: function (error) {
                console.log(error);
            }
        });
    });
}

// Projects page
if (location.pathname.match(/\/tag$/i)) {
    $(document).ready(function () {
        setupTagSearch(createProjectTile);
    });
}

$(document).ready(function () {
    setupAreaSelection();
});
