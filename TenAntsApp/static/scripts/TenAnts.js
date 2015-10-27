
var TenAnts = (function() {

    // PRIVATE VARIABLES
        
    // The backend we'll use for Part 2. For Part 3, you'll replace this 
    // with your backend.
    var apiUrl = 'http://127.0.0.1:8000'// 'https://smileback-cs169.herokuapp.com'; 

    // FINISH ME (Task 4): You can use the default smile space, but this means
    //            that your new smiles will be merged with everybody else's
    //            which can get confusing. Change this to a name that 
    //            is unlikely to be used by others. 
    var smileSpace = 'monkey_cheese'; // The smile space to use. 'initial'


    var smiles; // smiles container, value set in the "start" method below
    var smileTemplateHtml; // a template for creating smiles. Read from index.html
                           // in the "start" method
    var create; // create form, value set in the "start" method below

    var signup_form, login_form;
      
   /**
    * HTTP GET request 
    * @param  {string}   url       URL path, e.g. "/api/smiles"
    * @param  {function} onSuccess   callback method to execute upon request success (200 status)
    * @param  {function} onFailure   callback method to execute upon request failure (non-200 status)
    * @return {None}
    */
   var makeGetRequest = function(url, onSuccess, onFailure) {
       $.ajax({
           type: 'GET',
           url: apiUrl + url,
           dataType: "json",
           success: onSuccess,
           error: onFailure
       });
   };

    /**
     * HTTP POST request
     * @param  {string}   url       URL path, e.g. "/api/smiles"
     * @param  {Object}   data      JSON data to send in request body
     * @param  {function} onSuccess   callback method to execute upon request success (200 status)
     * @param  {function} onFailure   callback method to execute upon request failure (non-200 status)
     * @return {None}
     */
    var makePostRequest = function(url, data, onSuccess, onFailure) {
        $.ajax({
            type: 'POST',
            url: apiUrl + url,
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
            success: onSuccess,
            error: onFailure
        });
    };

    var doNothing_success = function(data) {};
    var doNothing_failure = function() {};

    var show_errors = function(data) {
        error_str = ''
        for (var i = data.errors.length - 1; i >= 0; i--) {
            console.error(data.errors[i]);
            error_str += data.errors[i] + "\n"
        };
        alert(error_str);
    }

    var login_onSuccess = function(data) {
        if (data.status == -1) {
            show_errors(data);
        } else {
            /* TODO: Redirect logged in user to dashboard. */
            window.location.href = apiUrl
        }
    };
    var login_onFailure = function() {
        alert('ERROR: Login Failed from Server')
        console.error('ERROR: SERVER ERROR');
    };

    var attachLogin = function(e) {
        $(".login_btn").on('click', function(e) {
            var account_json = {};
            account_json.email = login_form.find('#email_LI').val();
            account_json.password = login_form.find('#password_LI').val();

            makePostRequest('/api/login', account_json, login_onSuccess, login_onFailure)
        });
    };

    var attachSignUp = function(e) {

        $("#signup_btn").on('click', function(e) {
            var account_json = {};
            account_json.first_name = signup_form.find('#first_name_SU').val();
            account_json.last_name = signup_form.find('#last_name_SU').val();
            account_json.email = signup_form.find('#email_SU').val();
            account_json.password = signup_form.find('#password_SU').val();
            
            var onSuccess = function(data) {
                if (data.status == -1) {
                    show_errors(data);
                } else {
                    /* Subsequently login new user */
                    makePostRequest('/api/login', account_json, login_onSuccess, login_onFailure)
                }
            };
            var onFailure = function() {
                alert('ERROR: Account could not be created')
                console.error('ERROR: Account could not be created'); 
            };

            makePostRequest('/api/account', account_json, onSuccess, onFailure)
        });
    };

    
    /**
     * Start the app by displaying the most recent smiles and attaching event handlers.
     * @return {None}
     */
    var start = function() {
        signup_form = $(".signup_form");
        login_form = $(".login_form");
        
        attachSignUp();
        attachLogin();
    };
    

    // PUBLIC METHODS
    // any private methods returned in the hash are accessible via Smile.key_name, e.g. Smile.start()
    return {
        start: start
    };
    
})();
