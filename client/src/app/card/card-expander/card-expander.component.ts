import { Component, OnInit } from '@angular/core';

@Component({
	selector: 'app-card-expander',
	templateUrl: './card-expander.component.html',
	styleUrls: ['./card-expander.component.css']
})
export class CardExpanderComponent implements OnInit {

	constructor() { }

	ngOnInit(): void {
	}

	expand() {
		console.log('expand');
	}
}
