import { Component, OnInit } from '@angular/core';
import { Cube } from "../cube.type";
import cards from 'src/app/library/cards.json';
import { CubeService } from "../cube.service";

@Component({
  selector: 'app-cube-overview',
  templateUrl: './cube-overview.component.html',
  styleUrls: ['./cube-overview.component.css']
})
export class CubeOverviewComponent implements OnInit {
  cube: Cube;
  cubeName: string = "To be announced";
  noCards: boolean = true;

  constructor(
	  private cubeService: CubeService,
  ) { }

  ngOnInit(): void {
	this.cubeService.cube.subscribe(newCube => {
	  this.cube = newCube;
	  console.log("we arrive here!")
	  this.noCards = this.cube.cards.length == 0;
	  this.cubeName = newCube.name;
	})
  }

  changeName() {
	console.log("You pressed cube name!")
  }
}
