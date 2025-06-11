import { Component, ElementRef, EventEmitter, OnInit, Output, ViewChild } from '@angular/core';
import { TabsComponent } from '../tabs/tabs.component';
import { AgGridModule } from 'ag-grid-angular';
import { ColDef } from 'ag-grid-community';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ClientsService } from '../services/clientsService/clients.service';
import { N8nService } from '../services/n8n/n8n.service';
import { LoaderComponent } from '../loader/loader.component';
import { ChatComponent } from '../chat/chat.component';

interface ChatMessage {
  text: string;
  isUser: boolean;
  timestamp: Date;
}

export interface Client {
  id: string;
  documentType: string;
  documentId: string;
  fullName: string;
  dateOfBirth: string;
  gender: string;
  address: string;
  status: string
}

@Component({
  selector: 'app-customers',
  imports: [TabsComponent, AgGridModule, CommonModule, FormsModule, AgGridModule, LoaderComponent, ChatComponent],
  templateUrl: './customers.component.html',
  styleUrls: ['./customers.component.scss'],
  standalone: true,

})

export class CustomersComponent implements OnInit {

  constructor(private router: Router, private clientsService: ClientsService, private n8nService: N8nService) { }

  @Output() tabChanged = new EventEmitter<{ tab: string; clientId: string | null }>();

  @ViewChild('chatMessages') private chatMessagesContainer!: ElementRef;

  rowData: Client[] = [];
  loading: boolean = false;

  ngOnInit(): void {
    this.loading = true; 
    this.clientsService.getClientsData().subscribe({
      next: (data) => {
        (Array.isArray(data) ? data : []).forEach((ele: any) => {
          let client: Client = {
            id: ele.id || '',
            documentType: ele.kycDetails[0]?.documentType || '--',
            documentId: ele.kycDetails[0]?.documentId || '--',
            fullName: ele.kycDetails[0]?.fullName || '--',
            dateOfBirth: ele.kycDetails[0]?.dateOfBirth || '--',
            gender: ele.kycDetails[0]?.gender || '--',
            address: ele.kycDetails[0]?.address || '--',
            status: ele.kycDetails[0]?.status || '--',
          };
          this.rowData.push(client);
        });
        this.rowData = [...this.rowData];
        this.loading = false; 
      },
      error: (error) => {
        console.error('Error fetching clients data:', error);
      }});
  }

  clientId: string = '';

  messages: ChatMessage[] = [
    {
      text: 'Hello! How can I help you today?',
      isUser: false,
      timestamp: new Date(),
    },
  ];

  currentMessage: string = '';
  private shouldScrollToBottom = false;

  // New property to control chat visibility
  isChatOpen: boolean = false;

  sendMessage(): void {
    const message = this.currentMessage.trim();

    if (message) {
      // Add user message
      this.messages.push({
        text: message,
        isUser: true,
        timestamp: new Date(),
      });

      // Clear input
      this.currentMessage = '';
      this.shouldScrollToBottom = true;

      //Simulate bot response
      setTimeout(() => {
        this.messages.push({
          text: `Thanks for your message: "${message}". How else can I assist you?`,
          isUser: false,
          timestamp: new Date(),
        });
        this.shouldScrollToBottom = true;
      }, 1000);
    }
  }

  handleKeyPress(event: KeyboardEvent): void {
    if (event.key === 'Enter') {
      this.sendMessage();
    }
  }

  // New method to toggle chat visibility
  toggleChat(): void {
    this.isChatOpen = !this.isChatOpen;
    if (this.isChatOpen) {
      // Scroll to bottom when chat opens
      setTimeout(() => {
        this.shouldScrollToBottom = true;
      }, 100);
    }
  }

  ngAfterViewChecked(): void {
    if (this.shouldScrollToBottom) {
      this.scrollToBottom();
      this.shouldScrollToBottom = false;
    }
  }

  private scrollToBottom(): void {
    try {
      if (this.chatMessagesContainer) {
        this.chatMessagesContainer.nativeElement.scrollTop =
          this.chatMessagesContainer.nativeElement.scrollHeight;
      }
    } catch (err) {
      console.error('Error scrolling to bottom:', err);
    }
  }

  columnDefs: ColDef[] = [

    {
      headerName: 'Client ID',
      field: 'id',
      cellRenderer: (params:any) => {
        return `<a href="/portfolio?id=${params.value}" class="client-link">${params.value}</a>`;
      },
      cellStyle: { display: 'flex', alignItems: "center" }
    },
    { headerName: 'Document Type', field: 'documentType', cellStyle: { display: 'flex', alignItems: "center" } },
    { headerName: 'Document ID', field: 'documentId', cellStyle: { display: 'flex', alignItems: "center" } },
    { headerName: 'Full Name', field: 'fullName', cellStyle: { display: 'flex', alignItems: "center" } },
    { headerName: 'Date of Birth', field: 'dateOfBirth', cellStyle: { display: 'flex', alignItems: "center" } },
    { headerName: 'Gender', field: 'gender', cellStyle: { display: 'flex', alignItems: "center" } },
    { headerName: 'Address', field: 'address', cellStyle: { display: 'flex', alignItems: "center" } },
    {
      headerName: 'Status',
      field: 'status',
      cellStyle: { display: 'flex', alignItems: "center" }
    }
  ];

  // rowData = [
  //   {
  //     id: 'CLT-456', //make it hyperlink then go to portfolio
  //     documentType: 'AADHAR',
  //     documentId: '123456789001',
  //     fullName: 'John Doe',
  //     dateOfBirth: '01-01-1990',
  //     gender: 'Male',
  //     address: 'Kharadi, Pune, India'
  //   },
  //   {
  //     id: 'CLT-123',
  //     documentType: 'AADHAR',
  //     documentId: '123456789001',
  //     fullName: 'John Doe',
  //     dateOfBirth: '01-01-1990',
  //     gender: 'Male',
  //     address: 'Kharadi, Pune, India'
  //   }
  // ];

  // onGridReady(params: any) {
  //   params.api.sizeColumnsToFit();
  //   // Or, for best fit per column:
  //   const allColumnIds: string[] = [];
  //   params.columnApi.getAllColumns().forEach((column: any) => {
  //     allColumnIds.push(column.getId());
  //   });
  //   params.columnApi.autoSizeColumns(allColumnIds, false);
  // }

  onGridReady(params: any) {
    params.api.sizeColumnsToFit();
    const allColumnIds: string[] = [];
    params.columnApi.getAllColumns().forEach((column: any) => {
      allColumnIds.push(column.getId());
    });
    params.columnApi.autoSizeColumns(allColumnIds, false);
    // Add event delegation for link clicks
    const gridElement = document.querySelector('#table2');
    gridElement?.addEventListener('click', (event: any) => {
      const target = event.target as HTMLElement;
      if (target.classList.contains('client-link')) {
        event.preventDefault();
        const clientId = target.getAttribute('data-id');

        // Change tab and add query parameter
        this.router.navigate([], {
          queryParams: { clientId },
          queryParamsHandling: 'merge'
        });
      }
    });
  }


  defaultColDef = {
    flex: 1,
  };

  statusBar = {
    statusPanels: [
      {
        statusPanel: 'agTotalAndFilteredRowCountComponent',
        align: 'left',
      },
    ],
  };
} 