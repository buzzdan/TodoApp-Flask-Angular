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



angular.module('MyApp').controller('NewListController',['$scope','$rootScope', '$http',function ($scope, $rootScope, $http) {
  //$scope.newTodoList=  {};
  newTodoList = {name : 'dan'};
  $scope.newTodoList = newTodoList;

  $scope.authenticate = function(){
    $rootScope.$broadcast("login");
  }

  $scope.createNewList = function(listName){
        $http.post('/api/todolists', {'listName': listName})
            .success(function(newCreatedList) {
                console.log(newCreatedList);
                $rootScope.$broadcast("newListCreated", newCreatedList);
            })
            .error(function(data) {
                console.log('Error: ' + data);
            });
    }
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