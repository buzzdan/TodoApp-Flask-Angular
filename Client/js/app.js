console.log('hi ' + appConfigs.env);
angular.module('MyApp', ['ngResource', 'ui.bootstrap','ngMessages', 'ui.router', 'mgcrea.ngStrap', 'satellizer', 'newListModalService'])
  .config(function($stateProvider, $urlRouterProvider, $authProvider, $modalProvider) {

    angular.extend($modalProvider.defaults, {
        html: true
    });

    $stateProvider
      .state('home', {
        url: '/',
        templateUrl: 'js/partials/home.html',
        controller: 'mainController'
      })
      .state('login', {
        url: '/login',
        templateUrl: 'js/satellizer/partials/login.html',
        controller: 'LoginCtrl'
      })
      .state('signup', {
        url: '/signup',
        templateUrl: 'js/satellizer/partials/signup.html',
        controller: 'SignupCtrl'
      })
      .state('logout', {
        url: '/logout',
        template: null,
        controller: 'LogoutCtrl'
      })
      .state('profile', {
        url: '/profile',
        templateUrl: 'js/satellizer/partials/profile.html',
        controller: 'ProfileCtrl',
        resolve: {
          authenticated: function($q, $location, $auth) {
            var deferred = $q.defer();

            if (!$auth.isAuthenticated()) {
              $location.path('/login');
            } else {
              deferred.resolve();
            }

            return deferred.promise;
          }
        }
      });

    $urlRouterProvider.otherwise('/');

    $authProvider.facebook({
        clientId: appConfigs.facebookClientId
    });

    $authProvider.google({
      clientId: appConfigs.googleClientId
    });

    $authProvider.github({
      clientId: '45ab07066fb6a805ed74'
    });

    $authProvider.linkedin({
      clientId: '77cw786yignpzj'
    });

    $authProvider.yahoo({
      clientId: 'dj0yJmk9SDVkM2RhNWJSc2ZBJmQ9WVdrOWIzVlFRMWxzTXpZbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD0yYw--'
    });

    $authProvider.twitter({
      url: '/auth/twitter'
    });

    $authProvider.live({
      clientId: '000000004C12E68D'
    });

    $authProvider.oauth2({
      name: 'foursquare',
      url: '/auth/foursquare',
      clientId: 'MTCEJ3NGW2PNNB31WOSBFDSAD4MTHYVAZ1UKIULXZ2CVFC2K',
      redirectUri: window.location.origin || window.location.protocol + '//' + window.location.host,
      authorizationEndpoint: 'https://foursquare.com/oauth2/authenticate'
    });
  });