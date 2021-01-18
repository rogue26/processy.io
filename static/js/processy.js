// Edit type by converting to input field
function editType(event) {
    event.preventDefault();
    var $el = $(this);
    var $input = $('<input/>').val( $el.text() );
    $input.width( 300 )
    $el.replaceWith( $input );

    $input.on({
        keyup: function (e) { if (e.keyCode == 13) {save()}},
        blur: function (e) {save()}
    }).focus();

    function save(){
        var newval = $(this.target).val()

        var $a = $("<a/>").text( $input.val() );
        $a.attr("href","#");
        $a.attr("data-editable","");
        $a.attr("data-url",$el["data-url"]);
        $a.attr("modelid",$el.modelid);

        $input.replaceWith( $a );

        // update the database
        $.ajax({
            headers: {"X-CSRFToken": event.data.token},
            type: "POST",
            url: $el.attr('data-url'),
            data: {
                modelid: $el.attr('modelid'),
                newval: newval
            },
            success: function(data) {}
        });
    };
};

// Add new type above the "Add new" link - used to add workstream, deliverable, and task types in the org dashboard
function addNewTypeAbove(event){
    console.log('addNewTypeAbove?');
    event.preventDefault();
    var $el = $(this);
    var $input = $('<input/>');
    $newfield = $input
                    .insertBefore( $el.parents().eq(2) )
                    .wrap( "<div class=\"row\"></div>" )
                    .wrap( "<div class=\"col-md-12\"></div>" )
                    .wrap( "<div class=\"float-left\"></div>" );

    var $newdeleteicon = $('<a href="#" delete-item></a>');

    var $newdeleteicon = $("<a/>").insertAfter($newfield);
    $newdeleteicon.html('<span class="fa fa-minus-circle ml-2"></span>');
    $newdeleteicon.attr("href","#");
    $newdeleteicon.attr("delete-item","");

    // delete-button data-url stored in the delete-data-url attribute of the "add new" button
    $newdeleteicon.attr("data-url",$el["data-url"]);
    // note: modelid will be added after the ajax call is successful, since we don't know the ID yet.

    // Hide add-new button while input being edited. Effectively, only create one new item at a time.
    $(this).hide();

    var save = function(){
        $el.show();

        var newval = $input.val();

        var $a = $("<a/>").text( $input.val() );
        $a.attr("href","#");
        $a.attr("data-editable","");
        $a.attr("data-url",$el["data-url"]);
        // note: modelid will be added after the ajax call is successful, since we don't know the ID yet.

        $input.replaceWith( $a );

        // update the database
        $.ajax({
            headers: {"X-CSRFToken": event.data.token},
            type: "POST",
            url: $el.attr("data-url"),
            data: { newval: newval },
            success: function(data) {
                $a.attr("modelid",data);
                $newdeleteicon.attr("modelid",data)
            }
        });
    };
    $input.on({
        keyup: function (e) { if (e.keyCode == 13) {save()}},
        blur: function (e) {save()}
    }).focus();
};

// Add new row in table above the "Add new" link - used to add workstream, deliverable, and task types in the org dashboard
function addNewTypeAboveRow(event){
    console.log('addNewTypeAboveRow?');
    event.preventDefault();
    var $el = $(this);

    // create variable for current row with "add new" link
    var $addNewRow = $(this).closest('tr')

    // clone previous row
    var $prevRow    = $(this).closest('tr').prev();
    var $newRow = $prevRow.clone().insertAfter($prevRow);

    // hide the "add new" row
    $addNewRow.hide();

    // convert text to input field in $newRow
    $olda = $newRow.find('a').first();
    $deleteButton = $olda.next();

    var $input = $('<input/>');
    $newfield = $input
                    .insertBefore( $el.parents().eq(2) )
                    .wrap( "<div class=\"row\"></div>" )
                    .wrap( "<div class=\"col-md-12\"></div>" )
                    .wrap( "<div class=\"float-left\"></div>" );

    $olda.replaceWith( $newfield );
    $deleteButton.hide();


    var save = function(){
        $el.show();

        var newval = $input.val();

        var $newa = $("<a/>").text( $input.val() );
        $newa.attr("href","#");
        $newa.attr("data-editable","");
        $newa.attr("data-url",$el["data-url"]);
        // note: modelid will be added after the ajax call is successful, since we don't know the ID yet.

        $input.replaceWith( $newa );

        // update the database
        $.ajax({
            headers: {"X-CSRFToken": event.data.token},
            type: "POST",
            url: $el.attr("data-url"),
            data: { newval: newval },
            success: function(data) {
                $newa.attr("modelid",data);
                $deleteButton.attr("modelid",data)
                $deleteButton.show();
                $addNewRow.show()
            }
        });
    };
    $input.on({
        keyup: function (e) { if (e.keyCode == 13) {save()}},
        blur: function (e) {save()}
    }).focus();
};

// Add new type below the "Add new" link - used to add workstream, deliverable, and task types within modals
function addNewTypeBelow(event){
    event.preventDefault();
    var $el = $(this);
    var $input = $('<input/>');
    console.log('addNewTypeBelow?');

    $selectorFormRow = $el.closest('div[class^="form-row"]')
    $selector =$el.parent().prev().find(">:first-child")
    $newfield = $input
                    .addClass("form-control mt-3")
                    .attr('maxlength',"50")
                    .attr('type', "text")
                    .attr("placeholder", "Enter name of new type")
                    .insertAfter($selectorFormRow)
                    .wrap( "<div class=\"form-row\"></div>" )
                    .wrap( "<div class=\"col-md-12\"></div>" );


    // Hide add-new button while input being edited. Effectively, only create one new item at a time.
    $(this).hide();

    var save = function(){
        $el.show();

        var newval = $input.val();

        // add newval to dropdown options and select
        $newOption = $('<option>', {
            value: newval,
            text: newval,
            selected: true
        });

        $selector.append($newOption);

        $newfield.remove()

        // update the database
        $.ajax({
            headers: {"X-CSRFToken": event.data.token},
            type: "POST",
            url: $el.attr("data-url"),
            data: {newval: newval},
            success: function(data) {
                $newOption.attr('value', data);
            }
        })
    };
    $input.on({
        keyup: function (e) { if (e.keyCode == 13) {save()}},
        blur: function (e) {save()}
    }).focus();
};

// Delete spec type or condition type
function deleteType(event){
    event.preventDefault();
    var $el = $(this);

    $el.parents().eq(2).remove();

    // update the database
    $.ajax({
        headers: {"X-CSRFToken": event.data.token},
        type: "POST",
        url: $el.attr("data-url"),
        data: {modelid: $el.attr('modelid')},
        success: function(data) {}
    });
};

function deleteTypeRow(event){
    event.preventDefault();
    var $el = $(this);
    $el.closest('tr').remove();

    // update the database
    $.ajax({
        headers: {"X-CSRFToken": event.data.token},
        type: "POST",
        url: $el.attr("data-url"),
        data: {modelid: $el.attr('modelid')},
        success: function(data) {}
    });
};