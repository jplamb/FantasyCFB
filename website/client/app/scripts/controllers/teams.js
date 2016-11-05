'use strict';

/**
 * @ngdoc function
 * @name FFL.controller:teams
 * @description
 * # Teams
 * Controller of the FFL
 */
 
angular.module('clientApp')
  .controller('teamsController', function() {
    this.teamsList = [
      {
          name: 'John',
          points: 322
      },
      {
          name: 'Scott',
          points: 207
      }
    ];
});