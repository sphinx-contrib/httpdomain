"""The WebSocket domain for documenting bidirectional connections."""

from dataclasses import dataclass
from hashlib import sha256

from docutils import nodes

from sphinx import addnodes
from sphinx.directives import ObjectDescription, directives
from sphinx.domains import Domain, Index, ObjType
from sphinx.locale import get_translation
from sphinx.roles import XRefRole
from sphinx.util import logging
from sphinx.util.docfields import GroupedField, TypedField
from sphinx.util.nodes import make_refnode

from ._path_signature import render_path_signature


_ = get_translation('httpdomain')
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ConnectionRecord:
    """The persisted, indexed data for one WebSocket connection."""

    docname: str
    synopsis: str
    deprecated: bool


def connection_anchor(raw_signature):
    """Return the stable anchor for an indexed WebSocket connection."""
    slug = nodes.make_id(raw_signature) or 'connection'
    digest = sha256(raw_signature.encode('utf-8')).hexdigest()
    return 'websocket-%s-%s' % (slug, digest)


class WebSocketConnection(ObjectDescription):
    """Describe a WebSocket connection at an application path."""

    doc_field_types = [
        TypedField('parameter', label=_('Parameters'), names=('param',)),
        TypedField('queryparameter', label=_('Query Parameters'), names=('query',)),
        GroupedField('servermessage', label=_('Messages sent by server'),
                     names=('server-message',)),
        GroupedField('clientmessage', label=_('Messages sent by client'),
                     names=('client-message',)),
    ]

    option_spec = {
        'deprecated': directives.flag,
        'noindex': directives.flag,
        'no-index': directives.flag,
        'addtoc': directives.flag,
        'synopsis': lambda value: value,
    }

    def run(self):
        # Sphinx 6 only recognizes ``noindex``.  Sphinx 9 accepts both names,
        # but normalizing here keeps the documented spelling cross-version.
        if 'no-index' in self.options:
            self.options['noindex'] = self.options.pop('no-index')
        return super().run()

    def handle_signature(self, sig, signode):
        if not sig.startswith('/'):
            _, line = self.get_source_info()
            logger.warning(
                'WebSocket connection paths must begin with "/": %s', sig,
                location=(self.env.docname, line),
            )
            raise ValueError

        prefix = 'WebSocket '
        signode += addnodes.desc_name(prefix, prefix)
        render_path_signature(sig, signode)
        signode['path'] = sig
        signode['fullname'] = prefix + sig
        return sig

    def needs_arglist(self):
        return False

    def add_target_and_index(self, name, sig, signode):
        connections = self.env.domaindata['websocket']['connections']
        record = ConnectionRecord(
            self.env.docname,
            self.options.get('synopsis', ''),
            'deprecated' in self.options,
        )
        previous = connections.get(sig)
        if previous is not None:
            _, line = self.get_source_info()
            logger.warning(
                'duplicate WebSocket connection definition %s in %s; '
                'existing definition is in %s. Use :noindex: for an '
                'intentional secondary rendering.',
                sig,
                self.env.doc2path(self.env.docname),
                self.env.doc2path(previous.docname),
                location=(self.env.docname, line),
            )
            return
        signode['ids'].append(connection_anchor(sig))
        connections[sig] = record

    def get_index_text(self, modname, name):
        return ''

    def _object_hierarchy_parts(self, sig_node):
        if ('addtoc' not in self.options or 'noindex' in self.options or
                'no-index' in self.options):
            return ()
        path = sig_node.get('path')
        if not path:
            return ()
        return tuple(part for part in path.split('/') if part) + (
            'WebSocket ' + path,
        )

    def _toc_entry_name(self, sig_node):
        if not sig_node.get('_toc_parts'):
            return ''
        return sig_node['_toc_parts'][-1]


class WebSocketXRefRole(XRefRole):
    """Cross-reference a WebSocket connection."""

    def process_link(self, env, refnode, has_explicit_title, title, target):
        if not has_explicit_title:
            title = 'WebSocket ' + title
        return title, target


class WebSocketIndex(Index):
    """Generated index of indexed WebSocket connections."""

    name = 'routingtable'
    localname = _('WebSocket Routing Table')
    shortname = _('WebSocket routing table')

    @staticmethod
    def grouping_prefix(path):
        parts = [part for part in path.split('/') if part]
        return '/%s' % (parts[0] if parts else '')

    def generate(self, docnames=None):
        content = {}
        for path, record in sorted(self.domain.connections.items()):
            entries = content.setdefault(self.grouping_prefix(path), [])
            entries.append([
                'WebSocket ' + path,
                0,
                record.docname,
                connection_anchor(path),
                '',
                _('Deprecated') if record.deprecated else '',
                record.synopsis,
            ])
        return sorted(content.items()), True


class WebSocketDomain(Domain):
    """WebSocket documentation domain."""

    name = 'websocket'
    label = 'WebSocket'
    data_version = 1

    object_types = {
        'connection': ObjType('connection', 'connection'),
    }
    directives = {
        'connection': WebSocketConnection,
    }
    roles = {
        'connection': WebSocketXRefRole(),
    }
    initial_data = {
        'connections': {},
    }
    indices = [WebSocketIndex]

    @property
    def connections(self):
        return self.data['connections']

    def clear_doc(self, docname):
        for signature, record in list(self.connections.items()):
            if record.docname == docname:
                del self.connections[signature]

    def resolve_xref(self, env, fromdocname, builder, typ, target,
                     node, contnode):
        if not target.startswith('/'):
            logger.warning(
                'WebSocket connection targets must begin with "/": %s',
                target,
                location=node,
            )
            return contnode

        record = self.connections.get(target)
        if record is None:
            return contnode
        return make_refnode(
            builder,
            fromdocname,
            record.docname,
            connection_anchor(target),
            contnode,
            'WebSocket ' + target,
        )

    def resolve_any_xref(self, env, fromdocname, builder, target, node,
                         contnode):
        return []

    def get_objects(self):
        for signature, record in self.connections.items():
            yield (
                signature,
                signature,
                'connection',
                record.docname,
                connection_anchor(signature),
                1,
            )

    def merge_domaindata(self, docnames, otherdata):
        for signature, record in otherdata['connections'].items():
            previous = self.connections.get(signature)
            if previous is not None and previous != record:
                logger.warning(
                    'duplicate WebSocket connection definition %s in %s; '
                    'existing definition is in %s. Use :noindex: for an '
                    'intentional secondary rendering.',
                    signature,
                    self.env.doc2path(record.docname),
                    self.env.doc2path(previous.docname),
                )
                continue
            self.connections[signature] = record
