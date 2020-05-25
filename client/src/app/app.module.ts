import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './nav/navbar/navbar.component';
import { LibraryOverviewComponent } from './library/library-overview/library-overview.component';
import { HomeComponent } from './splashscreen/home/home.component';
import { CardFrontComponent } from './card/card-front/card-front.component';

@NgModule({
	declarations: [
		AppComponent,
		NavbarComponent,
		LibraryOverviewComponent,
		HomeComponent,
		CardFrontComponent
	],
	imports: [
		BrowserModule,
		AppRoutingModule
	],
	providers: [],
	bootstrap: [AppComponent]
})
export class AppModule { }
