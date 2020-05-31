import { Component, OnInit } from '@angular/core';
import { GameService } from 'src/app/game/game.service';

@Component({
	selector: 'app-home',
	templateUrl: './home.component.html',
	styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

	constructor(private game: GameService) { }

	ngOnInit(): void {
		this.game.start();
	}

}
