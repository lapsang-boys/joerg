import { Component, OnInit } from '@angular/core';
import { GameService } from '../../game.service';
import { Choice } from 'src/app/game/types/choice.type';

@Component({
	selector: 'app-board',
	templateUrl: './board.component.html',
	styleUrls: ['./board.component.css']
})
export class BoardComponent implements OnInit {

	poleIndex: number;
	choice: Choice;

	constructor(private game: GameService) { }

	ngOnInit(): void {
		this.game.getObservableBoard().subscribe(board => {
			this.poleIndex = board.pole.index;
		});
		this.game.getObservableChoice().subscribe(choice => {
			this.choice = choice;
		});
	}

	next() {
		this.game.next();
	}

	choose(choiceIndex: number): void {
		this.game.makeChoice(choiceIndex);
	}
}
