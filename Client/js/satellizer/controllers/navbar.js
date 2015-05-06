angular.module('MyApp')
  .controller('NavbarCtrl', function($scope, $auth, Account) {
    var isGettingUser = false;
    var gotUser = false;
    $scope.isAuthenticated = function() {
      var isAuthenticated = $auth.isAuthenticated();
      if(isAuthenticated && !gotUser && !isGettingUser){
        isGettingUser = true;
        GetLoggedInUser();
      }
      return isAuthenticated;
    };

    var GetLoggedInUser = function(){
      Account.getProfile()
        .success(function(data) {
          $scope.user = data;
          if(data.picture.indexOf("?type=large") > -1){
            $scope.user.picture = data.picture.replace("?type=large","");
          }
          gotUser = true;
          isGettingUser = false;
        })
        .error(function(error) {
          gotUser = false;
          $alert({
            content: error.message,
            animation: 'fadeZoomFadeDown',
            type: 'material',
            duration: 3
          });
        });
    }
  });