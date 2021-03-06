import { gettext } from "django";
import { customElement, html, property, TemplateResult } from "lit-element";
import { AKResponse } from "../../api/Client";
import { TableColumn } from "../../elements/table/Table";
import { TablePage } from "../../elements/table/TablePage";

import "../../elements/buttons/ModalButton";
import "../../elements/buttons/SpinnerButton";
import "../../elements/buttons/Dropdown";
import { until } from "lit-html/directives/until";
import { Stage } from "../../api/Flows";

@customElement("ak-stage-list")
export class StageListPage extends TablePage<Stage> {
    pageTitle(): string {
        return "Stages";
    }
    pageDescription(): string | undefined {
        return "Stages are single steps of a Flow that a user is guided through.";
    }
    pageIcon(): string {
        return "pf-icon pf-icon-plugged";
    }
    searchEnabled(): boolean {
        return true;
    }

    @property()
    order = "name";

    apiEndpoint(page: number): Promise<AKResponse<Stage>> {
        return Stage.list({
            ordering: this.order,
            page: page,
            search: this.search || "",
        });
    }

    columns(): TableColumn[] {
        return [
            new TableColumn("Name", "name"),
            new TableColumn("Flows"),
            new TableColumn(""),
        ];
    }

    row(item: Stage): TemplateResult[] {
        return [
            html`<div>
                <div>${item.name}</div>
                <small>${item.verbose_name}</small>
            </div>`,
            html`${item.flow_set.map((flow) => {
                return html`<a href="#/flow/flows/${flow.slug}">
                    <code>${flow.slug}</code>
                </a>`;
            })}`,
            html`
            <ak-modal-button href="${Stage.adminUrl(`${item.pk}/update/`)}">
                <ak-spinner-button slot="trigger" class="pf-m-secondary">
                    ${gettext("Edit")}
                </ak-spinner-button>
                <div slot="modal"></div>
            </ak-modal-button>
            <ak-modal-button href="${Stage.adminUrl(`${item.pk}/delete/`)}">
                <ak-spinner-button slot="trigger" class="pf-m-danger">
                    ${gettext("Delete")}
                </ak-spinner-button>
                <div slot="modal"></div>
            </ak-modal-button>
            `,
        ];
    }

    renderToolbar(): TemplateResult {
        return html`
        <ak-dropdown class="pf-c-dropdown">
            <button class="pf-m-primary pf-c-dropdown__toggle" type="button">
                <span class="pf-c-dropdown__toggle-text">${gettext("Create")}</span>
                <i class="fas fa-caret-down pf-c-dropdown__toggle-icon" aria-hidden="true"></i>
            </button>
            <ul class="pf-c-dropdown__menu" hidden>
                ${until(Stage.getTypes().then((types) => {
                    return types.map((type) => {
                        return html`<li>
                            <ak-modal-button href="${type.link}">
                                <button slot="trigger" class="pf-c-dropdown__menu-item">${type.name}<br>
                                    <small>${type.description}</small>
                                </button>
                                <div slot="modal"></div>
                            </ak-modal-button>
                        </li>`;
                    });
                }), html`<ak-spinner></ak-spinner>`)}
            </ul>
        </ak-dropdown>
        ${super.renderToolbar()}`;
    }

}
