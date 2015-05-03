angular.module('MyApp')
  .controller('mainController', function($scope, $alert, $auth, $http) {
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
  });