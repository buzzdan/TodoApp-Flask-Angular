angular.module('newListModalService',[]).
  service('$newListModal',function($modal){
    var myModal = $modal({template:'js/partials/createNewListModal.html', show:false});

    this.show=function(){
        myModal.$promise.then(myModal.show);
      }

    this.hide = function() {
        myModal.$promise.then(myModal.hide);
      }
  });



angular.module('MyApp').controller('NewListController',['$scope','$rootScope',function ($scope, $rootScope) {
  $scope.user=  {};

  $scope.authenticate = function(){
    $rootScope.$broadcast("login");
  }
  $scope.user = {name : ''};
//
//  $scope.cancel = function(){
//    myModal.$promise.then(myModal.hide);
//  }; // end cancel
//
//  $scope.save = function(){
//    $modalInstance.close($scope.user.name);
//  }; // end save
//
//  $scope.hitEnter = function(evt){
//    if(angular.equals(evt.keyCode,13) && !(angular.equals($scope.name,null) || angular.equals($scope.name,'')))
//				$scope.save();
//  }; // end hitEnter
}]);