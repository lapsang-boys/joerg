import { Component, OnInit } from '@angular/core';
import { GameService } from '../../game.service';

@Component({
	selector: 'app-board',
	templateUrl: './board.component.html',
	styleUrls: ['./board.component.css']
})
export class BoardComponent implements OnInit {

	poleIndex: number;

	constructor(private game: GameService) { }

	ngOnInit(): void {
		this.game.getObservableBoard().subscribe(board => {
			this.poleIndex = board.pole.index;
		});
	}

	next() {
		this.game.next();
	}

}
