var scotchTodo = angular.module('scotchTodo', []);

function mainController($scope, $http) {
    $scope.formData = {};

    // when landing on the page, get all todos and show them
    $http.get('/api/todos')
        .success(function(data) {
            $scope.todos = data;
            console.log(data);
        })
        .error(function(data) {
            console.log('Error: ' + data);
        });

    // when submitting the add form, send the text to the node API
    $scope.createTodo = function() {
        $http.post('/api/todos', $scope.formData)
            .success(function(data) {
                $scope.formData = {}; // clear the form so our user is ready to enter another
                $scope.todos = data;
                console.log(data);
            })
            .error(function(data) {
                console.log('Error: ' + data);
            });
    };

    var removeFromArray = function(array,id){
        var elementPos = array.map(function(x) {return x.id; }).indexOf(id)
        array.splice(elementPos, 1);
    }
    // delete a todo after checking it
    $scope.deleteTodo = function(id) {
        $http.delete('/api/todos/' + id)
            .success(function(data) {
                removeFromArray($scope.todos, id);
                console.log($scope.todos);
            })
            .error(function(data) {
                console.log('Error: ' + data);
            });
    };

}

// ========================================================= //
//
//angular.module('MyApp', ['ngResource', 'ngMessages', 'ui.router', 'mgcrea.ngStrap', 'satellizer'])
//  .config(function($stateProvider, $urlRouterProvider, $authProvider) {
//    $stateProvider
//      .state('home', {
//        url: '/',
//        templateUrl: 'partials/home.html'
//      })
//      .state('login', {
//        url: '/login',
//        templateUrl: 'partials/login.html',
//        controller: 'LoginCtrl'
//      })
//      .state('signup', {
//        url: '/signup',
//        templateUrl: 'partials/signup.html',
//        controller: 'SignupCtrl'
//      })
//      .state('logout', {
//        url: '/logout',
//        template: null,
//        controller: 'LogoutCtrl'
//      })
//      .state('profile', {
//        url: '/profile',
//        templateUrl: 'partials/profile.html',
//        controller: 'ProfileCtrl',
//        resolve: {
//          authenticated: function($q, $location, $auth) {
//            var deferred = $q.defer();
//
//            if (!$auth.isAuthenticated()) {
//              $location.path('/login');
//            } else {
//              deferred.resolve();
//            }
//
//            return deferred.promise;
//          }
//        }
//      });
//
//    $urlRouterProvider.otherwise('/');
//
//    $authProvider.facebook({
//      clientId: '603122136500203'
//    });
//
//    $authProvider.google({
//      clientId: '631036554609-v5hm2amv4pvico3asfi97f54sc51ji4o.apps.googleusercontent.com'
//    });
//
//    $authProvider.github({
//      clientId: '45ab07066fb6a805ed74'
//    });
//
//    $authProvider.linkedin({
//      clientId: '77cw786yignpzj'
//    });
//
//    $authProvider.yahoo({
//      clientId: 'dj0yJmk9SDVkM2RhNWJSc2ZBJmQ9WVdrOWIzVlFRMWxzTXpZbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD0yYw--'
//    });
//
//    $authProvider.twitter({
//      url: '/auth/twitter'
//    });
//
//    $authProvider.live({
//      clientId: '000000004C12E68D'
//    });
//
//    $authProvider.oauth2({
//      name: 'foursquare',
//      url: '/auth/foursquare',
//      clientId: 'MTCEJ3NGW2PNNB31WOSBFDSAD4MTHYVAZ1UKIULXZ2CVFC2K',
//      redirectUri: window.location.origin || window.location.protocol + '//' + window.location.host,
//      authorizationEndpoint: 'https://foursquare.com/oauth2/authenticate'
//    });
//  });
