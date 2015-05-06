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
          if(data.picture.contains("?type=large")){
            $scope.user.picture = data.picture.replace("?type=large","");
          }
        })
        .error(function(error) {
          $alert({
            content: error.message,
            animation: 'fadeZoomFadeDown',
            type: 'material',
            duration: 3
          });
        });
    }
  });