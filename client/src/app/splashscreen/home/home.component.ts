import { Component, OnInit } from '@angular/core';
import { SocketService } from 'src/app/network/socket.service';

@Component({
	selector: 'app-home',
	templateUrl: './home.component.html',
	styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

	constructor(private socket: SocketService) { }

	ngOnInit(): void {
		this.socket.go();
	}

}
