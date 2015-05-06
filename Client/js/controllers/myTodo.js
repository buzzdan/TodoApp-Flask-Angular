//var myApp = angular.module("MyApp",['newListModalService','mgcrea.ngStrap']);
angular.module('MyApp')
  .controller('mainController', function($scope, $alert, $auth, $http, $newListModal) {
    $scope.isAuthenticated = $auth.isAuthenticated();

    $scope.formData = {};

     // when landing on the page, get all todos and show them
    $http.get('/api/todolists')
        .success(function(data) {
            $scope.todoLists = data;
            console.log(data[0]);
        })
        .error(function(data) {
            console.log('Error: ' + data);
        });

    //MODAL
//    var myOtherModal = $modal({scope: $scope, template: 'js/partials/createNewListModal.html', show: false});
//    $scope.openNewListModal = function () {
//
//        myOtherModal.$promise.then(myOtherModal.show);
//    };
    //MODAL

    $scope.openNewListModal = function(){
        $newListModal.show();
    };
    $scope.$on("newListCreated", function(event, newCreatedList){
      $newListModal.hide();
      $scope.currentList = newCreatedList;
      $scope.todoLists.push(newCreatedList);
    });

     $scope.loadList = function(id) {
            $http.get('/api/todolists/'+id)
                .success(function(data) {
                    $scope.currentList = data;
                    console.log(data);
                })
                .error(function(data) {
                    console.log('Error: ' + data);
                });
        };

    $scope.status = {
        isopen: false
    };

    $scope.toggled = function(open) {
        console.log('Dropdown is now: ', open);
    };

    $scope.toggleDropdown = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.status.isopen = !$scope.status.isopen;
    };

    // when submitting the add form, send the text to the node API
    $scope.createTodo = function(listId) {
        $http.post('/api/todolists/'+listId, $scope.formData)
            .success(function(data) {
                $scope.formData = {}; // clear the form so our user is ready to enter another
                $scope.currentList = data;
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
    $scope.deleteTodo = function(listId, todoId) {
        $http.delete('/api/todolists/'+listId+'/todos/' + todoId)
            .success(function(data) {
                removeFromArray($scope.currentList.todos, todoId);
                console.log($scope.currentList.todos);
            })
            .error(function(data) {
                console.log('Error: ' + data);
            });
    };
  });