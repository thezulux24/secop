"""Output schema for one SECOP II contracting process record.

Field names mirror SECOP's own Spanish column names (camelCased) rather than translating
them, since the intended audience is Colombian analysts already familiar with SECOP's
terminology. All 59 source columns are mapped; numeric/date columns are cast from the
strings Socrata serializes them as.
"""

from __future__ import annotations

from datetime import date, datetime, timezone

from pydantic import BaseModel, ConfigDict, Field

from .soda import to_int, to_number, unwrap_url


def _now() -> datetime:
    return datetime.now(timezone.utc)


class Process(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra='ignore')

    # --- entity -----------------------------------------------------------
    entidad: str | None = None
    nit_entidad: str | None = Field(default=None, alias='nitEntidad')
    departamento_entidad: str | None = Field(default=None, alias='departamentoEntidad')
    ciudad_entidad: str | None = Field(default=None, alias='ciudadEntidad')
    orden_entidad: str | None = Field(default=None, alias='ordenEntidad')
    codigo_pci: str | None = Field(default=None, alias='codigoPci')
    codigo_entidad: str | None = Field(default=None, alias='codigoEntidad')

    # --- process identity ---------------------------------------------------
    id_del_proceso: str | None = Field(default=None, alias='idDelProceso')
    referencia_del_proceso: str | None = Field(default=None, alias='referenciaDelProceso')
    ppi: str | None = None
    id_del_portafolio: str | None = Field(default=None, alias='idDelPortafolio')
    nombre_del_procedimiento: str | None = Field(default=None, alias='nombreDelProcedimiento')
    descripcion_del_procedimiento: str | None = Field(default=None, alias='descripcionDelProcedimiento')
    fase: str | None = None
    estado_resumen: str | None = Field(default=None, alias='estadoResumen')
    estado_del_procedimiento: str | None = Field(default=None, alias='estadoDelProcedimiento')
    id_estado_del_procedimiento: str | None = Field(default=None, alias='idEstadoDelProcedimiento')
    estado_de_apertura_del_proceso: str | None = Field(default=None, alias='estadoDeAperturaDelProceso')

    # --- dates ---------------------------------------------------------------
    fecha_de_publicacion_del: date | None = Field(default=None, alias='fechaDePublicacionDel')
    fecha_de_ultima_publicacion: date | None = Field(default=None, alias='fechaDeUltimaPublicacion')
    fecha_de_publicacion_fase: date | None = Field(default=None, alias='fechaDePublicacionFase')
    fecha_de_publicacion_fase_1: date | None = Field(default=None, alias='fechaDePublicacionFase1')
    fecha_de_publicacion_fase_2: date | None = Field(default=None, alias='fechaDePublicacionFase2')
    fecha_de_publicacion_fase_3: date | None = Field(default=None, alias='fechaDePublicacionFase3')
    fecha_de_recepcion_de: date | None = Field(default=None, alias='fechaDeRecepcionDe')
    fecha_de_apertura_de_respuesta: date | None = Field(default=None, alias='fechaDeAperturaDeRespuesta')
    fecha_de_apertura_efectiva: date | None = Field(default=None, alias='fechaDeAperturaEfectiva')
    fecha_adjudicacion: date | None = Field(default=None, alias='fechaAdjudicacion')

    # --- economics -------------------------------------------------------------
    precio_base: float | None = Field(default=None, alias='precioBase')
    modalidad_de_contratacion: str | None = Field(default=None, alias='modalidadDeContratacion')
    justificacion_modalidad_de: str | None = Field(default=None, alias='justificacionModalidadDe')
    duracion: int | None = None
    unidad_de_duracion: str | None = Field(default=None, alias='unidadDeDuracion')
    tipo_de_contrato: str | None = Field(default=None, alias='tipoDeContrato')
    subtipo_de_contrato: str | None = Field(default=None, alias='subtipoDeContrato')
    codigo_principal_de_categoria: str | None = Field(default=None, alias='codigoPrincipalDeCategoria')
    categorias_adicionales: str | None = Field(default=None, alias='categoriasAdicionales')

    # --- unit responsible --------------------------------------------------------
    ciudad_de_la_unidad_de: str | None = Field(default=None, alias='ciudadDeLaUnidadDe')
    nombre_de_la_unidad_de: str | None = Field(default=None, alias='nombreDeLaUnidadDe')

    # --- participation / engagement -----------------------------------------------
    proveedores_invitados: int | None = Field(default=None, alias='proveedoresInvitados')
    proveedores_con_invitacion: int | None = Field(default=None, alias='proveedoresConInvitacion')
    visualizaciones_del: int | None = Field(default=None, alias='visualizacionesDel')
    proveedores_que_manifestaron: int | None = Field(default=None, alias='proveedoresQueManifestaron')
    respuestas_al_procedimiento: int | None = Field(default=None, alias='respuestasAlProcedimiento')
    respuestas_externas: int | None = Field(default=None, alias='respuestasExternas')
    conteo_de_respuestas_a_ofertas: int | None = Field(default=None, alias='conteoDeRespuestasAOfertas')
    proveedores_unicos_con: int | None = Field(default=None, alias='proveedoresUnicosCon')
    numero_de_lotes: int | None = Field(default=None, alias='numeroDeLotes')

    # --- award -----------------------------------------------------------------
    adjudicado: str | None = None
    id_adjudicacion: str | None = Field(default=None, alias='idAdjudicacion')
    valor_total_adjudicacion: float | None = Field(default=None, alias='valorTotalAdjudicacion')
    nombre_del_adjudicador: str | None = Field(default=None, alias='nombreDelAdjudicador')

    # --- awarded provider --------------------------------------------------------
    codigoproveedor: str | None = Field(default=None, alias='codigoProveedor')
    nombre_del_proveedor: str | None = Field(default=None, alias='nombreDelProveedor')
    nit_del_proveedor_adjudicado: str | None = Field(default=None, alias='nitDelProveedorAdjudicado')
    departamento_proveedor: str | None = Field(default=None, alias='departamentoProveedor')
    ciudad_proveedor: str | None = Field(default=None, alias='ciudadProveedor')

    # --- link -----------------------------------------------------------------------
    url_proceso: str | None = Field(default=None, alias='urlProceso')

    # --- provenance -------------------------------------------------------------
    search_keywords: str | None = Field(default=None, alias='searchKeywords')
    scraped_at: datetime = Field(default_factory=_now, alias='scrapedAt')

    @classmethod
    def from_soda_row(cls, row: dict, *, search_keywords: str | None = None) -> Process:
        """Build a Process from one raw SODA API row (all-string/mixed JSON)."""
        return cls(
            entidad=row.get('entidad'),
            nitEntidad=row.get('nit_entidad'),
            departamentoEntidad=row.get('departamento_entidad'),
            ciudadEntidad=row.get('ciudad_entidad'),
            ordenEntidad=row.get('ordenentidad'),
            codigoPci=row.get('codigo_pci'),
            codigoEntidad=row.get('codigo_entidad'),
            idDelProceso=row.get('id_del_proceso'),
            referenciaDelProceso=row.get('referencia_del_proceso'),
            ppi=row.get('ppi'),
            idDelPortafolio=row.get('id_del_portafolio'),
            nombreDelProcedimiento=row.get('nombre_del_procedimiento'),
            descripcionDelProcedimiento=row.get('descripci_n_del_procedimiento'),
            fase=row.get('fase'),
            estadoResumen=row.get('estado_resumen'),
            estadoDelProcedimiento=row.get('estado_del_procedimiento'),
            idEstadoDelProcedimiento=row.get('id_estado_del_procedimiento'),
            estadoDeAperturaDelProceso=row.get('estado_de_apertura_del_proceso'),
            fechaDePublicacionDel=row.get('fecha_de_publicacion_del'),
            fechaDeUltimaPublicacion=row.get('fecha_de_ultima_publicaci'),
            fechaDePublicacionFase=row.get('fecha_de_publicacion_fase'),
            fechaDePublicacionFase1=row.get('fecha_de_publicacion_fase_1'),
            fechaDePublicacionFase2=row.get('fecha_de_publicacion_fase_2'),
            fechaDePublicacionFase3=row.get('fecha_de_publicacion_fase_3'),
            fechaDeRecepcionDe=row.get('fecha_de_recepcion_de'),
            fechaDeAperturaDeRespuesta=row.get('fecha_de_apertura_de_respuesta'),
            fechaDeAperturaEfectiva=row.get('fecha_de_apertura_efectiva'),
            fechaAdjudicacion=row.get('fecha_adjudicacion'),
            precioBase=to_number(row.get('precio_base')),
            modalidadDeContratacion=row.get('modalidad_de_contratacion'),
            justificacionModalidadDe=row.get('justificaci_n_modalidad_de'),
            duracion=to_int(row.get('duracion')),
            unidadDeDuracion=row.get('unidad_de_duracion'),
            tipoDeContrato=row.get('tipo_de_contrato'),
            subtipoDeContrato=row.get('subtipo_de_contrato'),
            codigoPrincipalDeCategoria=row.get('codigo_principal_de_categoria'),
            categoriasAdicionales=row.get('categorias_adicionales'),
            ciudadDeLaUnidadDe=row.get('ciudad_de_la_unidad_de'),
            nombreDeLaUnidadDe=row.get('nombre_de_la_unidad_de'),
            proveedoresInvitados=to_int(row.get('proveedores_invitados')),
            proveedoresConInvitacion=to_int(row.get('proveedores_con_invitacion')),
            visualizacionesDel=to_int(row.get('visualizaciones_del')),
            proveedoresQueManifestaron=to_int(row.get('proveedores_que_manifestaron')),
            respuestasAlProcedimiento=to_int(row.get('respuestas_al_procedimiento')),
            respuestasExternas=to_int(row.get('respuestas_externas')),
            conteoDeRespuestasAOfertas=to_int(row.get('conteo_de_respuestas_a_ofertas')),
            proveedoresUnicosCon=to_int(row.get('proveedores_unicos_con')),
            numeroDeLotes=to_int(row.get('numero_de_lotes')),
            adjudicado=row.get('adjudicado'),
            idAdjudicacion=row.get('id_adjudicacion'),
            valorTotalAdjudicacion=to_number(row.get('valor_total_adjudicacion')),
            nombreDelAdjudicador=row.get('nombre_del_adjudicador'),
            codigoProveedor=row.get('codigoproveedor'),
            nombreDelProveedor=row.get('nombre_del_proveedor'),
            nitDelProveedorAdjudicado=row.get('nit_del_proveedor_adjudicado'),
            departamentoProveedor=row.get('departamento_proveedor'),
            ciudadProveedor=row.get('ciudad_proveedor'),
            urlProceso=unwrap_url(row.get('urlproceso')),
            searchKeywords=search_keywords,
        )

    def to_dataset(self) -> dict:
        return self.model_dump(by_alias=True, mode='json')
