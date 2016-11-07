'use strict';

/**
 * @ngdoc function
 * @name clientApp.controller:AboutCtrl
 * @description
 * # AboutCtrl
 * Controller of the clientApp
 */
angular.module('clientApp')
  .controller('AboutCtrl', function ($scope) {
    $scope.teamsList = [
        {
          name: 'John',
          points: 42
        },
        {
          name: 'Jack',
          points: 35
        }

      ];
  });
